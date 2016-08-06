import pandas
import wikischolar


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
    page = wikischolar.util.get_page(title)
    revision_gen = page.revisions(content=content)
    # hack to turn pywikibot.Revisions into records for pandas
    revision_list = [revision.__dict__ for revision in revision_gen]
    revisions = pandas.DataFrame.from_records(revision_list)
    revisions.insert(0, 'title', title)
    return revisions
