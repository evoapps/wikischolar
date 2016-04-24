#!/usr/bin/env python
from invoke import task, run, Collection

from .get import get
from .article_quality import article_quality
from .publish import publish


@task
def clean():
    """Remove junk files."""
    cmd = 'rm -rf {}'
    patterns = ['*.lwp', 'apicache', 'throttle.ctrl']
    for pattern in patterns:
        run(cmd.format(pattern))


namespace = Collection(clean, get, article_quality, publish)
