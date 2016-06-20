import logging
import sqlite3

import pywikibot
import pandas
import pypandoc
import unipath


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
