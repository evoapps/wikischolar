import sys

from invoke import task, run, Collection
import pandas
import unipath

from . import get, fill, quality, edits, views, generations
from . import R
from .util import mkdir, save, read

# DRY docs
ARTICLES = "Article title or path to csv of articles with titles."
OUTPUT = "Optional path to new csv to save. By default output goes to stdout."
SINGLE = "If specified, input is a single value rather than a path."


@task(aliases=['save'],
      help={'output': 'Name of sqlite file to save to.',
            'force': 'Should any existing data be removed? Default is False.'})
def save_all_revisions(articles, output='revisions.sqlite', single=False,
                       force=False):
    """Retrieve all revisions from a list of titles."""
    output = unipath.Path(output)
    if force and output.exists():
        output.remove()
    articles = read(articles, single, 'title')
    get.save_all_revisions(articles, db_name=output)


@task(aliases=['get'],
      help=dict(title="The title of the wiki page", output=OUTPUT))
def get_table(title, output=None):
    """Retrieve a table of articles from a wiki page."""
    table = get.get_table(title)
    save(table, output)


@task(aliases=['fill'],
      help=dict(articles=ARTICLES, output=OUTPUT))
def fill_yearly_ids(articles, output=None, single=False):
    """Retrieve the revision ids for each article sampled at year's end."""
    articles = read(articles, single, 'title')
    revids = fill.fill_yearly_ids(articles)
    save(revids, output)


@task(aliases=['quality'],
      help=dict(revisions="Path to an existing csv of revisions with revids.",
                output=OUTPUT, single=SINGLE))
def wp10_qualities(revisions, output=None, single=False):
    """Obtain article quality estimates from the ORES."""
    unassessed = read(revisions, single, 'revid')
    qualities = quality.wp10_qualities(unassessed)
    save(qualities, output)


@task(aliases=['edits'],
      help=dict(articles=ARTICLES, output=OUTPUT, single=SINGLE))
def count_yearly_edits(articles, output=None, single=False):
    """Count edits per year for each article."""
    articles = read(articles, single, 'title')
    counts = edits.count_yearly_edits(articles)
    save(counts, output)


@task(aliases=['generations'],
      help=dict(articles=ARTICLES, output=OUTPUT, single=SINGLE))
def count_yearly_generations(articles, output=None, single=False):
    """Fold revisions into an evolutionary tree and count the generations."""
    articles = read(articles, single, 'title')
    counts = generations.count_yearly_generations(articles)
    save(counts, output)


@task(aliases=['views'],
      help=dict(articles=ARTICLES, output=OUTPUT, single=SINGLE))
def yearly_page_views(articles, output=None, single=False):
    """Get yearly page view sums for each article."""
    articles = read(articles, single, 'title')
    totals = views.yearly_page_views(articles)
    save(totals, output)


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
    count_yearly_generations,
    yearly_page_views,
    save_all_revisions,
)
