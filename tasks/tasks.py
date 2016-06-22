import sys
import sqlite3
import logging
logger = logging.getLogger(__name__)

from invoke import task, run, Collection
import pandas
import unipath

import tasks as wikischolar

from .revisions import (save_all_revisions, checkout_all_revisions,
                        resample_revisions)
from .edits import count_yearly_edits
from .quality import wp10_qualities
from .util import read

DB_NAME = 'wikischolar.sqlite'
MISSING_DB_MSG = 'no database at {}'


@task
def query(sql, database=None, output=None):
    """Query the wikischolar database."""
    db_loc = unipath.Path(database or DB_NAME)
    output = output or sys.stdout

    assert db_loc.exists(), MISSING_DB_MSG.format(db_loc)

    db = sqlite3.connect(db_loc)
    try:
        results = pandas.read_sql_query(sql, db)
    finally:
        db.close()

    results.to_csv(output)


@task
def revisions(articles, database=None, purge=False, split_char='|',
              title_col='title'):
    """Get all versions of articles and save them in a local db.

    Download the revisions for a single article like this::

        $ inv revisions "Splendid fairywren"

    By default the revisions are stored in a local sqlite database. Specify
    a database name manually with the ``--database`` option::

        $ inv revisions "Splendid fairywren" -d data/wikischolar.sqlite

    You can include multiple titles if they are separated in some way. By
    default the pipe character is expected::

        $ inv revisions "Splendid Fairywren|Field trip|Basketball"

    A much easier way is to provide a file of articles to retrieve.
    If a csv is provided, a column containing article titles is expected.
    By default, the expected name is 'title' but this can be specified
    on the command line::

        $ inv revisions data/articles.csv --title-col=name

    By default, the new revisions are appended to an existing database. If
    the ``--purge`` flag is provided, the output database is removed if it
    exists, and the results are stored in a fresh database::

        $ inv revisions data/articles.csv --purge -d data/wikischolar.sqlite
    """
    db_loc = unipath.Path(database or DB_NAME)

    if unipath.Path(articles).exists():
        articles = pandas.read_csv(articles)  # might fail
        titles = articles[title_col].tolist() # might fail
    else:
        titles = articles.split(split_char)   # should always produce list

    if purge and db_loc.exists():
        db_loc.remove()

    db = sqlite3.connect(db_loc)
    try:
        save_all_revisions(titles, db)
    finally:
        db.close()


@task
def edits(database=None):
    """Tally the number of yearly edits from a list of articles."""
    db_loc = unipath.Path(database or DB_NAME)
    assert db_loc.exists(), MISSING_DB_MSG.format(db_loc)

    db = sqlite3.connect(db_loc)
    try:
        all_revisions = checkout_all_revisions(db)
        counts = count_yearly_edits(all_revisions)
        counts.to_sql('edits', db, if_exists='append', index=False)
    finally:
        db.close()


@task
def qualities(database=None, resample_offset='YearEnd'):
    """Filter a subset of revisions and save the results in a new table."""
    db_loc = unipath.Path(database or DB_NAME)
    assert db_loc.exists(), MISSING_DB_MSG.format(db_loc)
    offset = getattr(pandas.tseries.offsets, resample_offset)()

    db = sqlite3.connect(db_loc)
    try:
        sample = resample_revisions(db, offset)
        sample = sample[['title', 'timestamp', 'revid']]
        qualities = wp10_qualities(sample)
        qualities.to_sql('qualities', db, if_exists='append', index=False)
    finally:
        db.close()


# @task(aliases=['get'],
#       help=dict(title="The title of the wiki page", output=OUTPUT))
# def get_table(title, output=None):
#     """Retrieve a table of articles from a wiki page."""
#     table = get.get_table(title)
#     save(table, output)
#
#
# @task(aliases=['fill'],
#       help=dict(articles=ARTICLES, output=OUTPUT))
# def fill_yearly_ids(articles, output=None, single=False):
#     """Retrieve the revision ids for each article sampled at year's end."""
#     articles = read(articles, single, 'title')
#     revids = fill.fill_yearly_ids(articles)
#     save(revids, output)
#
#
# @task(aliases=['quality'],
#       help=dict(revisions="Path to an existing csv of revisions with revids.",
#                 output=OUTPUT, single=SINGLE))
# def wp10_qualities(revisions, output=None, single=False):
#     """Obtain article quality estimates from the ORES."""
#     unassessed = read(revisions, single, 'revid')
#     qualities = quality.wp10_qualities(unassessed)
#     save(qualities, output)
#
#
# @task(aliases=['generations'],
#       help=dict(articles=ARTICLES, output=OUTPUT, single=SINGLE))
# def count_yearly_generations(articles, output=None, single=False):
#     """Fold revisions into an evolutionary tree and count the generations."""
#     articles = read(articles, single, 'title')
#     counts = generations.count_yearly_generations(articles)
#     save(counts, output)
#
#
# @task(aliases=['views'],
#       help=dict(articles=ARTICLES, output=OUTPUT, single=SINGLE))
# def yearly_page_views(articles, output=None, single=False):
#     """Get yearly page view sums for each article."""
#     articles = read(articles, single, 'title')
#     totals = views.yearly_page_views(articles)
#     save(totals, output)
#
#
# @task
# def clean():
#     """Remove junk files."""
#     cmd = 'rm -rf {}'
#     patterns = [
#         # wiki
#         'apicache',
#         'throttle.ctrl',
#         '*.lwp',
#
#         # knitr
#         '*-figs/',
#     ]
#     for pattern in patterns:
#         run(cmd.format(pattern))


namespace = Collection(
    revisions,
    edits,
    query,
    qualities,
)
