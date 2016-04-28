from concurrent import futures
import functools

from invoke import task
import pywikibot
import pandas

MAX_WORKERS = 20

@task
def fill_ids(articles, period, output):
    """Retrieve the revision ids for each article sampled periodically."""
    if period == 'yearly':
        offset = pandas.tseries.offsets.YearEnd()
    else:
        raise NotImplementedError

    articles = pandas.read_csv(articles)
    get_periodic_revisions = functools.partial(sample_revisions, offset=offset)
    workers = min(MAX_WORKERS, len(articles))

    with futures.ThreadPoolExecutor(workers) as executor:
        revisions = executor.map(get_periodic_revisions, articles.itertuples())

    pandas.concat(revisions).to_csv(output, index=False)


def sample_revisions(article, offset):
    """Sample the revisions for an article at a given offset."""
    title = article.article
    revisions = get_revisions(title)
    revisions.set_index('timestamp', inplace=True)
    sample = revisions.resample(offset).last()
    sample.reset_index(inplace=True)
    sample.insert(0, 'article', title)
    return sample


def get_revisions(title, drop_na=True):
    """Get all of the revisions for an article.

    Revisions without revids are dropped by default.
    """
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    # hack to turn pywikibot Revisions into records for pandas
    revision_list = [revision.__dict__ for revision in page.revisions()]
    revisions = pandas.DataFrame.from_records(revision_list)
    if drop_na:
        revisions.dropna(subset=['revid'], inplace=True)
    return revisions
