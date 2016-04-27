#!/usr/bin/env python
from invoke import task, run, Collection

from .get import get_table
from .fill import fill_ids
from .quality import quality


@task
def clean():
    """Remove junk files."""
    cmd = 'rm -rf {}'
    patterns = ['*.lwp', 'apicache', 'throttle.ctrl']
    for pattern in patterns:
        run(cmd.format(pattern))


namespace = Collection(get_table, fill_ids, quality, clean)
