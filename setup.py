from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='winterwizardjam',
    version='0.1.0',
    description='A game created for the Winter Wizard Jam.',
    long_description=long_description,
    url='https://github.com/TeamAwesomeTOJam/winterwizardjam',
    author='Team Awesome',
    author_email='',

    keywords='game wizardjam kitesurfing',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['sdl2hl', 'requests'],
    package_data = {
        'winterwizardjam': ['res/*/*'],
    },
    entry_points={
        'gui_scripts': [
            'winterwizardjam=winterwizardjam:main',
        ],
    },
)

