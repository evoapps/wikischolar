#!/usr/bin/env python
from invoke import task, run, Collection

from . import R
from .get import get_table
from .fill import fill_yearly_ids
from .quality import wp10_quality
from .edits import count_yearly_edits


@task
def clean():
    """Remove junk files."""
    cmd = 'rm -rf {}'
    patterns = [
        # wiki
        'apicache',
        'throttle.ctrl',
        '*.lwp',

        # knitr
        '*-figs/',
    ]
    for pattern in patterns:
        run(cmd.format(pattern))


namespace = Collection(
    # modules
    R,
    # local tasks
    clean,
    # wikischolar tasks
    get_table,
    fill_yearly_ids,
    wp10_quality,
    count_yearly_edits,
)
