import pywikibot
import pandas
import unipath


def get_page(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page


def get_revisions(title):
    """Get all of the revisions for an article.

    Requires pywikibot to be configured properly.

    Args:
        title (str): Name of the Wikipedia article.
    Returns:
        A pandas.DataFrame of revisions.
    """
    page = get_page(title)
    # hack to turn pywikibot Revisions into records for pandas
    revision_list = [revision.__dict__ for revision in page.revisions()]
    revisions = pandas.DataFrame.from_records(revision_list)
    return revisions


def mkdir(dst):
    dst_dir = unipath.Path(dst).parent
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True)
