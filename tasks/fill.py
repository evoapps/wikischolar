from concurrent import futures
import functools
import time

from invoke import task
import pywikibot
import pandas

from .util import get_revisions

MAX_WORKERS = 4
CURRENT_YEAR = time.localtime().tm_year


def fill_yearly_ids(articles):
    """Get the last revid of each year of an article's existence.

    Args:
        articles (pandas.DataFrame): A table of articles with titles.
    Returns:
        A pandas.DataFrame of article titles with year end revids.
    """
    offset = pandas.tseries.offsets.YearEnd()
    sample_revisions_yearly = functools.partial(sample_revisions, offset=offset)
    workers = min(MAX_WORKERS, len(articles))

    with futures.ThreadPoolExecutor(workers) as executor:
        results = executor.map(sample_revisions_yearly, articles.itertuples())
    return pandas.concat(results)


def sample_revisions(article, offset):
    """Sample the revisions for an article at a given offset."""
    title = article.title

    try:
        revisions = get_revisions(title)
    except pywikibot.NoPage:
        return pandas.DataFrame()

    revisions.set_index('timestamp', inplace=True)
    sample = revisions.resample(offset).last()

    # Fill missing revids for years w/o edits with the previous year's revid
    sample['revid'] = sample.revid.fillna(method='bfill').astype(int)

    # Drop this year's edits
    last_valid_edit_date = '{}-12-31'.format(CURRENT_YEAR-1)
    sample = sample.ix[:last_valid_edit_date]

    sample.reset_index(inplace=True)
    return sample
