import logging
import sqlite3

import pywikibot
import pandas

from .util import get_page

logger = logging.getLogger(__name__)

DB_TABLE = 'revisions'


def save_all_revisions(titles, db):
    """Retrieve revisions for all titles and save to the db."""
    # NB: Not trying this multithreaded because I doubt pandas+sqlite
    #     can handle simultaneous writes.
    for title in titles:
        save_revisions(title, db)


def checkout_all_revisions(db):
    sql_query = 'SELECT * FROM {}'.format(DB_TABLE)
    revisions = pandas.read_sql_query(sql_query, db)
    # sqlite doesn't have a timestamp format
    revisions['timestamp'] = pandas.to_datetime(revisions.timestamp)
    return revisions


def save_revisions(title, db, table=None):
    """Retrieve a table of article revisions and store them locally."""
    table = table or DB_TABLE

    try:
        revisions = get_revisions(title, content=True)
    except pywikibot.NoPage:
        msg = 'Revisions requested for {} but no page was found'
        logger.debug(msg.format(title))
        revisions = None

    try:
        revisions.to_sql(table, db, if_exists='append', index=False)
    except AttributeError as e:
        msg = 'Error saving revisions for {} to db: {}'
        logger.debug(msg.format(title, e))

    return revisions


def get_revisions(title, content=False):
    """Get all of the revisions for an article.

    Requires pywikibot to be configured properly.

    Args:
        title (str): Name of the Wikipedia article.
        content (bool): Should the article text content of the revision be
            retrieved? Default is to retrieve just metadata.
    Returns:
        A pandas.DataFrame of revisions.
    """
    page = get_page(title)
    revision_gen = page.revisions(content=content)
    # hack to turn pywikibot.Revisions into records for pandas
    revision_list = [revision.__dict__ for revision in revision_gen]
    revisions = pandas.DataFrame.from_records(revision_list)
    revisions.insert(0, 'title', title)
    return revisions
