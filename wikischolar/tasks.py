import sys
import logging
logger = logging.getLogger(__name__)

from invoke import task, run, Collection
import pandas
import unipath

import wikischolar

ARTICLES_TABLE = 'articles'
REVISIONS_TABLE = 'revisions'
EDITS_TABLE = 'edits'
GENERATIONS_TABLE = 'generations'
VIEWS_TABLE = 'views'


@task
def load(ctx, articles, database=None, table=None, title_col='title',
         split_char='|'):
    """Populate a new wikischolar database with articles to study.

    Args:
        articles (str): Article title or titles, separated by ``split_char``.
            Can also be a path to a csv of articles.
        database (str): Path to sqlite database to use. Defaults to
            a database named "wikischolar.sqlite" in the current directory.
        table (str): Name of the table in the db in which to save the articles.
            By default the table is named 'articles'.
        title_col (str): If ``articles`` is a path to a csv, ``title_col``
            specifies which column contains the article titles.
        split_char (str): If multiple articles are specified, ``split_char``
            determines how to split them into a list of articles.

    This function is meant to be used on the command line as an invoke task.

    Load an article from it's title::

        $ inv load "Splendid fairywren"

    By default the revisions are stored in a local sqlite database. Specify
    a database name manually with the ``--database`` option::

        $ inv load "Splendid fairywren" -d data/wikischolar.sqlite

    You can include multiple titles if they are separated in some way. By
    default the pipe character is expected::

        $ inv load "Splendid Fairywren|Field trip|Basketball"
        $ inv load "Splendid fairywren;Field trip;Basketball" --split-char=';'

    A much easier way is to provide a file of articles to retrieve.
    If a csv is provided, a column containing article titles is expected.
    By default, the expected name is 'title' but this can be specified
    on the command line::

        $ inv load data/articles.csv
        $ inv load other-data/names.csv --title-col=name

    By default the articles are stored in a table named 'articles'. This
    can be changed using the ``--table`` option::

        $ inv load "Splendid fairywren" --table=birds
    """
    if unipath.Path(articles).exists():
        articles = pandas.read_csv(articles)  # might fail
        articles.rename(columns={title_col: 'title'}, inplace=True)
    else:
        titles = articles.split(split_char)   # should always produce a list
        articles = pandas.DataFrame({'title': titles})

    db = wikischolar.db.connect(database, must_exist=False)
    table = table or ARTICLES_TABLE
    try:
        articles.to_sql(table, db, if_exists='append', index=False)
    finally:
        db.close()


@task
def dump(ctx, table, database=None, output=None):
    """Dump a table of the (local) wikischolar database."""
    sql_query = 'SELECT * FROM {};'
    output = output or sys.stdout
    db = wikischolar.db.connect(database)
    try:
        results = pandas.read_sql_query(sql_query.format(table), db)
    finally:
        db.close()

    results.to_csv(output)


@task
def revisions(ctx, database=None, articles_table=None):
    """Get all versions of articles and save them in a local db."""
    titles_query = 'SELECT DISTINCT title FROM {};'
    articles_table = articles_table or ARTICLES_TABLE
    db = wikischolar.db.connect(database)
    try:
        titles = wikischolar.db.query(titles_query.format(articles_table), db)
        wikischolar.revisions.save_all_revisions(titles, db)
    finally:
        db.close()


@task
def edits(ctx, database=None):
    """Tally the number of yearly edits from a list of articles."""
    db = wikischolar.db.connect(database)
    try:
        all_revisions = wikischolar.revisions.checkout_all_revisions(db)
        counts = wikischolar.edits.count_yearly_edits(all_revisions)
        counts.to_sql('edits', db, if_exists='append', index=False)
    finally:
        db.close()


@task
def qualities(ctx, database=None, resample_offset='YearEnd'):
    """Filter a subset of revisions and save the results in a new table."""
    offset = getattr(pandas.tseries.offsets, resample_offset)()
    db = wikischolar.db.connect(database)
    try:
        sample = wikischolar.revisions.resample_revisions(db, offset)
        sample = sample[['title', 'timestamp', 'revid']]
        qualities = wikischolar.qualities.wp10_qualities(sample)
        qualities.to_sql('qualities', db, if_exists='append', index=False)
    finally:
        db.close()


@task
def generations(ctx, database=None):
    """Count the number of generations (edits excluding reversions)."""
    db = wikischolar.db.connect(database)
    try:
        all_revisions = wikischolar.revisions.checkout_all_revisions(db)
        counts = wikischolar.generations.count_yearly_generations(all_revisions)
        counts.to_sql('generations', db, if_exists='append', index=False)
    finally:
        db.close()


# @task(aliases=['views'],
#       help=dict(articles=ARTICLES, output=OUTPUT, single=SINGLE))
# def yearly_page_views(articles, output=None, single=False):
#     """Get yearly page view sums for each article."""
#     articles = read(articles, single, 'title')
#     totals = views.yearly_page_views(articles)
#     save(totals, output)


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
    load,
    revisions,
    qualities,
    edits,
    generations,
)