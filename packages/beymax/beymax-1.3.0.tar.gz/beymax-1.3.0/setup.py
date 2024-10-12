from setuptools import setup

with open('requirements.txt') as r:
	requirements = r.readlines()

with open('README.md') as r:
	readme = r.read()

from beymax import __version__

setup(
	name='beymax',
	version=__version__,
	packages=['beymax', 'beymax.control'],
	install_requires=requirements,
	classifiers=[
		"Development Status :: 5 - Production/Stable",

		"Framework :: AsyncIO",

		"Intended Audience :: Developers",

		"License :: OSI Approved :: MIT License",

		"Natural Language :: English",

		"Operating System :: OS Independent",

		"Programming Language :: Python :: 3 :: Only",

		"Topic :: Communications :: Chat",
		"Topic :: Internet",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Utilities"
	],
	author="Aaron Graubert",
	author_email="aaron@graubert.com",
	description="A high-level, functional programming wrapper to discord.py",
	long_description=readme,
	long_description_content_type='text/markdown',
	license='MIT',
	keywords='discord async asyncio sql sqlalchemy utilities',
	url='https://gitlab.graubert.com/agraubert/beymax'

)

