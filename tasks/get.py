import logging
import sqlite3

import pywikibot
import pandas
import pypandoc
import unipath

from .util import get_revisions


def save_all_revisions(articles, db_name):
    """Retrieve revisions for all titles and save to the db."""
    # NB: Not trying this multithreaded because I doubt pandas+sqlite
    #     can handle simultaneous writes.
    db = sqlite3.connect(db_name)
    try:
        for title in articles.title:
            cache_revisions(title, db)
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


def cache_revisions(title, db, table='revisions'):
    """Retrieve a table of article revisions and store them locally."""
    try:
        revisions = get_revisions(title, content=True)
    except pywikibot.NoPage:
        msg = 'Page views requested for {} but no page was found'
        # logging.debug(msg.format(title))
        print(msg, title)

    try:
        revisions.to_sql(table, db, if_exists='append', index=False)
    except AttributeError as e:
        msg = 'Error saving revisions for {} to db: {}'
        # logging.debug(msg.format(title, e))
        print(msg.format(title, e))


def get_table(title):
    """Retrieve a table of articles from a wiki page."""
    wiki_text = get_page_text(title)
    table = convert_wiki_to_table(wiki_text)
    data = tidy_wiki_table(table)
    return data


def get_page_text(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page.get()


def convert_wiki_to_table(wiki_text):
    html_text = pypandoc.convert(wiki_text, 'html', 'mediawiki')
    tables = pandas.read_html(html_text)
    table = tables[0]  # take the first table only
    return table


def tidy_wiki_table(table):
    slugify = lambda s: s.strip('|').lower().replace(' ', '_')
    data = table.rename(columns=slugify)
    return data
