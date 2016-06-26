from distutils.core import setup

setup(
    name='wikischolar',
    version='0.1.0',
    packages=['wikischolar'],
    install_requires=['invoke'],
    entry_points={
        'console_scripts': ['sch = wikischolar.main:program.run']
    },
)
