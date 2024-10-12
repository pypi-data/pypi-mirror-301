import logging
from textwrap import wrap
from unittest.mock import patch
import sqlalchemy.orm
import discord.app_commands
from discord.utils import MISSING

logger = logging.getLogger('beymax.core.suite')

class Schema(object):
    pass

class CommandSuite(object):
    def __init__(self, name, group_description=None, group_name=None, force_enable=False, metadata=None):
        self.name = name
        self.bot = None
        self.commands = []
        self.tasks = []
        self.special = []
        self.subscriptions = []
        self.migrations = []
        self.channels = []
        self.context = []
        self.schema = Schema()
        self.dependencies = []
        self.dependents = []
        self.tables = []
        self.command_group = None
        self.forced = force_enable
        self.metadata = metadata if metadata is not None else {}
        
        if self.forced:
            logger.info("Command suite {} marked as mandatory. Controllers should not disable this".format(self.name))
        
        if group_description is not None:
            logger.warning("Grouping commands in suite {}. Command permissions are fully grouped, so ensure it's okay to lose granular control".format(self.name))
            if group_name is None:
                group_name = name.lower().replace(' ', '_')[:32]
                logger.debug("A group description was provided with no name. Auto-generating name for suite {}".format(name))
            self.command_group = discord.app_commands.Group(
                name=group_name,
                description=group_description,
                default_permissions=discord.Permissions(use_application_commands=False)
            )
    
    def get_meta(self, key):
        return self.metadata[key] if key in self.metadata else None
    
    def add_dependency(self, suite):
        self.dependencies.append(suite)
        suite.dependents.append(self)

    def table(self, cls):
        """
        Declare a new table for the database.
        Guild tables MUST include a guild_id element and the /viewdb command will automatically
        filter guild tables to only elements from the current guild
        """
        if not hasattr(cls, 'guild_id'):
            raise TypeError("Guild-tables must contain a guild_id element")
        # Maybe no need for a schema event if the declarative base class is just globally available
        @self.subscribe('schema', once=True)
        async def add_table(bot, evt, db):
            class Table(db.base, cls):
                _table_original_name = cls.__name__
                _table_guild_scope = True
                # if hasattr(cls, '_relationships_'):
                #     for attr, val in cls._relationships_.items():
                #         setattr(Table, attr, sqlalchemy.orm.relationship(val))

            setattr(self.schema, cls.__name__, Table)
            cls._table = Table
        cls.table = lambda : cls._table
        cls._table = None
        self.tables.append(add_table)
        return cls
    
    def global_table(self, cls):
        """
        Declare a new table for the database.
        Guild tables MUST include a guild_id element and the /viewdb command will automatically
        filter guild tables to only elements from the current guild
        """
        # Maybe no need for a schema event if the declarative base class is just globally available
        @self.subscribe('schema', once=True)
        async def add_table(bot, evt, db):
            class Table(db.base, cls):
                _table_original_name = cls.__name__
                _table_guild_scope = False
                # if hasattr(cls, '_relationships_'):
                #     for attr, val in cls._relationships_.items():
                #         setattr(Table, attr, sqlalchemy.orm.relationship(val))

            setattr(self.schema, cls.__name__, Table)
            cls._table = Table
        cls.table = lambda : cls._table
        cls._table = None
        self.tables.append(add_table)
        return cls
    
    async def debug_schema(self, db):
        for table in self.tables:
            await table(None, None, db)

    def attach(self, bot):
        """
        Attaches this command suite to the given bot
        """
        if self.bot == bot or self.name in bot.suites:
            logger.info("Skipping suite {} (already enabled)".format(self.name))
            
        logger.info(
            "Enabling command suite {}: {} commands, {} context menus, {} tasks, {} special message handlers, {} event handlers, {} db migrations, {} channel references".format(
                self.name,
                len(self.commands),
                len(self.context),
                len(self.tasks),
                len(self.special),
                len(self.subscriptions),
                len(self.migrations),
                len(self.channels)
            )
        )

        for dependency in self.dependencies:
            dependency.attach(bot)

        self.bot = bot
        bot.suites[self.name] = self
        for channel in self.channels:
            bot.reserve_channel(channel)

        for migration in self.migrations:
            bot.migration(migration['key'])(migration['function'])

        for subscription in self.subscriptions:
            bot.subscribe(
                subscription['event'],
                condition=subscription['condition'],
                once=subscription['once']
            )(subscription['function'])

        for special in self.special:
            bot.add_special(special['checker'], flavor=special['flavor'])(special['function'])

        for task in self.tasks:
            bot.add_task(
                task['seconds'], minutes=task['minutes'], 
                hours=task['hours'], times=task['times'], 
                count=task['count'], reconnect=task['reconnect']
            )(task['function'])

        for command in self.commands:
            bot.add_command(command['command'], *command['args'], command_suite_group=self.command_group, _command_suite=self, **command['kwargs'])(command['function'])
        
        for ctx in self.context:
            bot.add_context(ctx['name'], *ctx['args'], _command_suite=self, **ctx['kwargs'])(ctx['function'])
        
        if self.command_group is not None:
            @bot.subscribe('before:command-init', once=True)
            async def add_command_group(bot, event):
                if len(self.command_group.commands):
                    bot.tree.add_command(
                        self.command_group,
                    )

    def add_command(self, command, *args, **kwargs):
        def wrapper(func):
            self.commands.append(
                {
                    'command': command,
                    'args': args,
                    'kwargs': kwargs,
                    'function': func
                }
            )
            return func
        return wrapper
    
    def add_context(self, name, *args, **kwargs):
        def wrapper(func):
            self.context.append({
                'name': name,
                'args': args,
                'kwargs': kwargs,
                'function': func
            })
            return func
        return wrapper

    def add_task(self, seconds=None, *, minutes=None, hours=None, times=None, count=None, reconnect=None):
        def wrapper(func):
            self.tasks.append(
                {
                    'seconds': seconds,
                    'minutes': minutes,
                    'hours': hours,
                    'times': times,
                    'count': count,
                    'reconnect': reconnect,
                    'function': func,
                }
            )
            return func
        return wrapper

    def add_special(self, checker, flavor='blind'):
        def wrapper(func):
            self.special.append(
                {
                    'checker': checker,
                    'function': func,
                    'flavor': flavor
                }
            )
            return func
        return wrapper

    def subscribe(self, event, *, condition=None, once=False):
        def wrapper(func):
            self.subscriptions.append(
                {
                    'event': event,
                    'function': func,
                    'condition': condition,
                    'once': once
                }
            )
            return func
        return wrapper

    def migration(self, key):
        """
        Migrations run after the bot has connected to discord and has readied.
        Discord interactions will be ready
        """
        def wrapper(func):
            self.migrations.append(
                {
                    'key': key,
                    'function': func
                }
            )
            return func
        return wrapper

    def reserve_channel(self, name):
        """
        Call to declare a channel reference. The bot configuration can then map
        this reference to an actual channel. By default all undefined references
        map to general
        Arguments:
        name : A string channel reference to reserve
        """
        self.channels.append(name)
