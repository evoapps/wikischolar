#!/usr/bin/env python
from invoke import Program

from . import tasks

program = Program(namespace=tasks, version='0.1.0')
