
import pywikibot
import pandas

from .util import get_page

DB_TABLE = 'revisions'


def save_all_revisions(articles, db_name):
    """Retrieve revisions for all titles and save to the db."""
    # NB: Not trying this multithreaded because I doubt pandas+sqlite
    #     can handle simultaneous writes.
    db = sqlite3.connect(db_name)
    try:
        for title in articles.title:
            save_revisions(title, db)
    finally:
        db.close()


def checkout_revisions(db_name, sql_select='*', sql_from='revisions'):
    db = sqlite3.connect(db_name)
    sql_query = 'SELECT {} from {};'.format(sql_select, sql_from)
    try:
        revisions = pandas.read_sql_query(sql_query, db)
    finally:
        db.close()
    return revisions


def save_revisions(title, db, table=None):
    """Retrieve a table of article revisions and store them locally."""
    table = table or DB_TABLE

    try:
        revisions = get_revisions(title, content=True)
    except pywikibot.NoPage:
        msg = 'Revisions requested for {} but no page was found'
        logging.error(msg.format(title))
        revisions = None

    try:
        revisions.to_sql(table, db, if_exists='append', index=False)
    except AttributeError as e:
        msg = 'Error saving revisions for {} to db: {}'
        logging.error(msg.format(title, e))

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
