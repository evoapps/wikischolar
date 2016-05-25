from invoke import task, run, Collection

import pandas

from . import get, fill, quality, edits, views
from . import R
from .util import mkdir

# DRY docs
ARTICLES = "Path to existing csv of articles with titles."
OUTPUT = "Path to new csv to save."


@task(aliases=['get'],
      help=dict(title="The title of the wiki page", output=OUTPUT))
def get_table(title, output):
    """Retrieve a table of articles from a wiki page."""
    table = get.get_table(title)
    mkdir(output)
    table.to_csv(output, index=False)


@task(aliases=['fill'],
      help=dict(articles=ARTICLES, output=OUTPUT))
def fill_yearly_ids(articles, output):
    """Retrieve the revision ids for each article sampled at year's end."""
    articles = pandas.read_csv(articles)
    revids = fill.fill_yearly_ids(articles)
    revids.to_csv(output, index=False)


@task(aliases=['quality'],
      help=dict(revisions="Path to an existing csv of revisions with revids.",
                output=OUTPUT))
def wp10_qualities(revisions, output):
    """Obtain article quality estimates from the ORES."""
    unassessed = pandas.read_csv(revisions)
    qualities = quality.wp10_qualities(unassessed)
    qualities.to_csv(output, index=False)


@task(aliases=['edits'],
      help=dict(articles=ARTICLES, output=OUTPUT))
def count_yearly_edits(articles, output):
    """Count edits per year for each article."""
    articles = pandas.read_csv(articles)
    counts = edits.count_yearly_edits(articles)
    counts.to_csv(output, index=False)


@task(aliases=['views'],
      help=dict(articles=ARTICLES, output=OUTPUT))
def yearly_page_views(articles, output):
    """Get yearly page view sums for each article."""
    articles = pandas.read_csv(articles)
    totals = views.yearly_page_views(articles)
    totals.to_csv(output, index=False)


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
