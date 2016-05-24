from setuptools import setup

setup(
    name='wikischolar',
    version='0.1.0',
    description='Look up historical Wikipedia article data',
    url='https://github.com/evoapps/wikischolar',
    author='Pierce Edmiston',
    author_email='pierce@evoapps.xyz',
    packages=['wikischolar'],
    entry_points={
        'console_scripts': ['scholar = wikischolar.main:program.run']
    }
)
