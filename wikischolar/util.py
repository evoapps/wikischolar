import sys

import pywikibot
import pandas
import unipath


def get_page(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page


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
