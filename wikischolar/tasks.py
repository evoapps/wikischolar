import sys
import logging

from invoke import task, Collection
import pandas

import wikischolar

logger = logging.getLogger(__name__)


@task
def checkout(ctx, articles, plugins=None, database=None):
    """Checkout revisions for articles and process them with plugins.

    Checks out revisions in chunks and passes each chunk through each
    of the plugins.

    This function is intended to be called with command line arguments.

    Args:
        articles (str): Path to a csv file of articles.
        plugins (str): Names of plugins to process each article.
        database (str): Name of sqlite database for storing the results.
    """
    articles = wikischolar.parser.load_articles(articles)
    revisions = wikischolar.parser.load_revisions(articles.title)
    plugins = wikischolar.parser.load_plugins(plugins.split(','))
    database = wikischolar.db.connect(database)
    for chunk in revisions:
        for plugin in plugins:
            try:
                plugin(chunk, database=database)
            except wikischolar.plugins.PluginError as err:
                logger.debug('PluginError: {}'.format(err))
    database.close()


@task
def get(ctx, title, output=None):
    """Get the content of a Wikipedia page from its title."""
    text = wikischolar.util.get_wiki(title)
    out = open(output, 'w') if output else sys.stdout
    out.write(text)
    out.close()


@task
def dump(ctx, table, select='*', database=None, output=None):
    """Dump a table of the (local) wikischolar database.

    Be careful when saving revisions table to file because the article
    content is included.

    Args:
        table (str): The name of the table to dump.
        select (str): The columns to select. Defaults to '*' (all columns).
        database (str): Path to sqlite database to use. Defaults to
            a database named "wikischolar.sqlite" in the current directory.
        output (str): Path to csv to save results. Defaults to ``stdout``.
    """
    output = output or sys.stdout
    sql_query = 'SELECT {} FROM {};'.format(select, table)

    db = wikischolar.db.connect(database)
    try:
        results = pandas.read_sql_query(sql_query, db)
    finally:
        db.close()

    results.to_csv(output)


@task
def execute(ctx, cmd, database=None):
    """Execute a command on the wikischolar db."""
    db = wikischolar.db.connect(database)
    try:
        c = db.cursor()
        c.execute(cmd)
        db.commit()
    finally:
        db.close()


namespace = Collection(
    get,
    checkout,
    dump,
    execute,
)
