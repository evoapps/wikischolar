from invoke import Program, Collection
from wikischolar.tasks import namespace

program = Program(namespace=namespace, version='0.1.0')
