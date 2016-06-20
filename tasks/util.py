import sys

import pywikibot
import pandas
import unipath


def get_page(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page


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
    # hack to turn pywikibot Revisions into records for pandas
    revision_list = [revision.__dict__ for revision in revision_gen]
    revisions = pandas.DataFrame.from_records(revision_list)
    revisions.insert(0, 'title', title)
    return revisions


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
