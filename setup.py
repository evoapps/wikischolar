
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wikischolar',
    version='0.1.0',
    description='Look up historical quality data on articles.',
    long_description=long_description,
    url='https://github.com/evoapps/wikischolar',
    author='Pierce Edmiston',
    author_email='pierce@evoapps.xyz',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='mediawiki ores',
    packages=['wikischolar'],
    install_requires=['invoke'],
    entry_points={
        'console_scripts': [
            'wikischolar=wikischolar.main:program.run',
        ],
    },
)
