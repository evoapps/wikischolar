from invoke import task

import pywikibot
import pandas
import pypandoc


@task
def get():
    """Retrieve a table of articles from a wiki page."""
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, 'User:Smallbones/1000_random#Data')
    mediawiki_text = page.text
    html_text = pypandoc.convert(mediawiki_text, 'html', 'mediawiki')
    data = pandas.read_html(html_text)
    data = data[0]  # take the first table only
    data.to_csv('1000_random.csv', index=False)
