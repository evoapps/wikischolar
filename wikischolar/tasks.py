#!/usr/bin/env python
from invoke import task, run
import wikivision

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


@task
def



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
