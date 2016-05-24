from invoke import Program
from wikischolar.tasks import namespace

program = Program(namespace=namespace, version='0.1.0')
