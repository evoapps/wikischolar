from concurrent import futures
import functools

from invoke import task

import pandas

from .util import get_revisions

MAX_WORKERS = 4


def count_yearly_edits(articles):
    """Get the yearly edit counts for each article in a table.

    Args:
        articles (pandas.DataFrame): A table of articles with titles.
    Returns:
        A pandas.DataFrame of edit counts for each year of each article's
        existence.
    """
    offset = pandas.tseries.offsets.YearEnd()
    count_edits_yearly = functools.partial(count_edits, offset=offset)
    workers = min(MAX_WORKERS, len(articles))

    with futures.ThreadPoolExecutor(workers) as executor:
        results = executor.map(count_edits_yearly, articles.itertuples())
    return pandas.concat(results)


def count_edits(article, offset):
    """Count the number of revisions for an article in a given timespan.

    Args:
        article: A named tuple containing the article title.
        offset: A pandas.tseries.offset to group revisions by.
    Returns:
        A pandas.DataFrame of edit counts for this article.
    """
    title = article.title
    revisions = get_revisions(title)

    revisions.set_index('timestamp', inplace=True)
    edits = revisions.resample(offset).count()

    edits.reset_index(inplace=True)
    edits.insert(0, 'title', title)
    return edits
