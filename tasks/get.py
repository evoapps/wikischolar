from invoke import task

import pywikibot
import pandas
import pypandoc


@task
def get():
    """Retrieve a table of articles from a wiki page."""
    wiki_text = get_page_text('User:Smallbones/1000_random#Data')
    data = convert_wiki_to_table(wiki_text)
    data.to_csv('1000_random.csv', index=False)


def get_page_text(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page.get()


def convert_wiki_to_table(wiki_text):
    html_text = pypandoc.convert(wiki_text, 'html', 'mediawiki')
    tables = pandas.read_html(html_text)
    data = tables[0]  # take the first table only
    return data
