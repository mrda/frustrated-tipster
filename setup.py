from setuptools import setup, find_packages

setup(
    name='frustrated-tipster',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['frustrated-tipster = frustrated_tipster.main:main']
        }
    )
