#!/usr/bin/env python
from invoke import task, run, Collection

from . import R
from .get import get_table
from .fill import fill_yearly_ids
from .quality import wp10_quality



@task
def clean():
    """Remove junk files."""
    cmd = 'rm -rf {}'
    patterns = ['*.lwp', 'apicache', 'throttle.ctrl']
    for pattern in patterns:
        run(cmd.format(pattern))


namespace = Collection(get_table, fill_yearly_ids, wp10_quality, clean, R)
