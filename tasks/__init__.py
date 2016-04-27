#!/usr/bin/env python
from invoke import task, run, Collection

from .get import get_table
from .quality import quality
from .publish import publish


@task
def clean():
    """Remove junk files."""
    cmd = 'rm -rf {}'
    patterns = ['*.lwp', 'apicache', 'throttle.ctrl']
    for pattern in patterns:
        run(cmd.format(pattern))


namespace = Collection(clean, get_table, quality, publish)
