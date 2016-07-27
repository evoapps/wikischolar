import sys

import pywikibot
import pandas
import unipath
import pypandoc


def get_page(title):
    """Returns a pywikibot.Page given a single title."""
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page


def get_wiki(title):
    """Returns the contents of a wiki page in wiki syntax."""
    return get_page(title).get()


def get_table(title):
    """Return the first table on a wiki page as a pandas.DataFrame."""
    wiki_text = get_wiki(title)
    table = convert_wiki_to_table(wiki_text)
    data = tidy_wiki_table(table)
    return data


def convert_wiki_to_table(wiki_text):
    html_text = pypandoc.convert(wiki_text, 'html', 'mediawiki')
    tables = pandas.read_html(html_text)
    table = tables[0]  # take the first table only
    return table


def tidy_wiki_table(table):
    slugify = lambda s: s.strip('|').lower().replace(' ', '_')
    data = table.rename(columns=slugify)
    return data



def mkdir(dst):
    dst_dir = unipath.Path(dst).parent
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True)


def save(frame, output=None):
    if output:
        mkdir(output)
    else:
        output = sys.stdout
    frame.to_csv(output, index=False)


def read(argv, is_value, name):
    """Create a table from a path or a value.

    >>> df = read('articles.csv', is_value=False, name='title')
    >>> df = read('Splendid fairywren', is_value=True, name='title')

    Args:
        argv (str): The unknown argument, e.g., from the command line.
        is_value (bool): Is argv supposed to be a value?
        name (str): The required column if argv is given as a value.
    """
    if is_value:
        return pandas.DataFrame({name: [argv]})
    else:
        return pandas.read_csv(argv)
