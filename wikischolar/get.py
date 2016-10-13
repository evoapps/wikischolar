import logging
import sqlite3

import pywikibot
import pandas
import pypandoc
import unipath

from .util import get_page


def get_table(title, n_table=0):
    """Retrieve a table of articles from a wiki page."""
    wiki_text = get_page(title).get()
    table = convert_wiki_to_table(wiki_text, n_table)
    data = tidy_wiki_table(table)
    return data


def convert_wiki_to_table(wiki_text, n_table=0):
    html_text = pypandoc.convert(wiki_text, 'html', 'mediawiki')
    tables = pandas.read_html(html_text)
    return tables[n_table]


def tidy_wiki_table(table):
    slugify = lambda s: s.strip('|').lower().replace(' ', '_')
    data = table.rename(columns=slugify)
    return data
