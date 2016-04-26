from invoke import task

import pywikibot
import pandas
import pypandoc
import unipath

DATA = unipath.Path('data')
if not DATA.exists():
    DATA.mkdir()


@task(help=dict(save_all="Write each stage of the pipeline to the data dir."))
def get(save_all=False):
    """Retrieve a table of articles from a wiki page."""
    wiki_text = get_page_text('User:Smallbones/1000_random#Data')
    data = convert_wiki_to_table(wiki_text)
    data.to_csv(unipath.Path(DATA, 'article_data.csv'), index=False)

    if save_all:
        unipath.Path(DATA, 'wiki_text.mediawiki').write_file(wiki_text)


def get_page_text(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page.get()


def convert_wiki_to_table(wiki_text):
    html_text = pypandoc.convert(wiki_text, 'html', 'mediawiki')
    tables = pandas.read_html(html_text)
    data = tables[0]  # take the first table only
    return data
