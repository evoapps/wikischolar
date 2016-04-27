from invoke import task

import pywikibot
import pandas
import pypandoc
import unipath

DATA = unipath.Path('data')
if not DATA.exists():
    DATA.mkdir()


@task
def get_table(title, output):
    """Retrieve a table of articles from a wiki page."""
    wiki_text = get_page_text(title)
    data = convert_wiki_to_table(wiki_text)

    dst = unipath.Path(output)
    if not dst.parent.exists():
        dst.parent.mkdir(True)

    data.to_csv(dst, index=False)


def get_page_text(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page.get()


def convert_wiki_to_table(wiki_text):
    html_text = pypandoc.convert(wiki_text, 'html', 'mediawiki')
    tables = pandas.read_html(html_text)
    data = tables[0]  # take the first table only
    return data
