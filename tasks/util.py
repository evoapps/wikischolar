import pywikibot
import pandas


def get_revisions(title):
    """Get all of the revisions for an article.

    Requires pywikibot to be configured properly.

    Args:
        title (str): Name of the Wikipedia article.
    Returns:
        A pandas.DataFrame of revisions.
    """
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    # hack to turn pywikibot Revisions into records for pandas
    revision_list = [revision.__dict__ for revision in page.revisions()]
    revisions = pandas.DataFrame.from_records(revision_list)
    return revisions
