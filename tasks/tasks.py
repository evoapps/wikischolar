import sys

from invoke import task, run, Collection
import pandas

from . import get, fill, quality, edits, views
from . import R
from .util import mkdir, save

# DRY docs
ARTICLES = "Path to existing csv of articles with titles."
OUTPUT = "Path to new csv to save."


@task(aliases=['get'],
      help=dict(title="The title of the wiki page", output=OUTPUT))
def get_table(title, output=None):
    """Retrieve a table of articles from a wiki page."""
    table = get.get_table(title)
    save(table, output)


@task(aliases=['fill'],
      help=dict(articles=ARTICLES, output=OUTPUT))
def fill_yearly_ids(articles, output=None):
    """Retrieve the revision ids for each article sampled at year's end."""
    articles = pandas.read_csv(articles)
    revids = fill.fill_yearly_ids(articles)
    save(revids, output)


@task(aliases=['quality'],
      help=dict(revisions="Path to an existing csv of revisions with revids.",
                output=OUTPUT))
def wp10_qualities(revisions, output=None):
    """Obtain article quality estimates from the ORES."""
    unassessed = pandas.read_csv(revisions)
    qualities = quality.wp10_qualities(unassessed)
    save(qualities, output)


@task(aliases=['edits'],
      help=dict(articles=ARTICLES, output=OUTPUT))
def count_yearly_edits(articles, output=None):
    """Count edits per year for each article."""
    articles = pandas.read_csv(articles)
    counts = edits.count_yearly_edits(articles)
    save(counts, output)


@task(aliases=['views'],
      help=dict(articles=ARTICLES, output=OUTPUT))
def yearly_page_views(articles, output=None):
    """Get yearly page view sums for each article."""
    articles = pandas.read_csv(articles)
    totals = views.yearly_page_views(articles)
    save(total, output)


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
    wp10_qualities,
    count_yearly_edits,
    yearly_page_views,
)
