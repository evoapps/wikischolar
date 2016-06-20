import sys

from invoke import task, run, Collection
import pandas
import unipath

from . import revisions, get, fill, quality, edits, views, generations
from . import R
from .util import mkdir, save, read

DB_NAME = 'wikischolar.sqlite'


# DRY docs
ARTICLES = "Article title or path to csv of articles with titles."
OUTPUT = "Optional path to new csv to save. By default output goes to stdout."
SINGLE = "If specified, input is a single value rather than a path."


@task(help=dict(articles=ARTICLES,
                output=('Name of sqlite file to save to.'
                        'Defaults to {}').format(DB_NAME),
                single=SINGLE,
                purge='Should any existing data be removed? Default is False.'))
def revisions(articles, output=None, single=False, purge=False):
    """Retrieve all revisions from a list of titles.

    Download the revisions for a list of articles like this::

        $ inv revisions data/articles.csv -o data/wikischolar.sqlite

    The articles.csv input is expected to have a column named title. Instead
    of getting the revisions for a list of articles, revisions for individual
    articles can be obtained as well using the ``single`` flag::

        $ inv revisions -s "Splendid fairywren" -o data/wikischolar.sqlite

    By default, the new revisions are appended to an existing database. If
    the ``--purge`` flag is provided, the output database is removed if it
    exists, and the results are stored in a fresh database and table::

        $ inv revisions data/articles.csv -p -o data/wikischolar.sqlite
    """
    output = unipath.Path(output or DB_NAME)
    if purge and output.exists():
        output.remove()
    articles = read(articles, single, 'title')
    revisions.save_all_revisions(articles, db_name=output)


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
    revisions,
)
