from concurrent import futures
import functools
import time

from invoke import task
import pywikibot
import pandas

MAX_WORKERS = 4
CURRENT_YEAR = time.localtime().tm_year

@task(aliases=['fill'])
def fill_yearly_ids(articles, output):
    """Retrieve the revision ids for each article sampled at year's end."""
    articles = pandas.read_csv(articles)

    offset = pandas.tseries.offsets.YearEnd()
    sample_revisions_yearly = functools.partial(sample_revisions, offset=offset)
    workers = min(MAX_WORKERS, len(articles))

    with futures.ThreadPoolExecutor(workers) as executor:
        revisions = executor.map(sample_revisions_yearly, articles.itertuples())

    pandas.concat(revisions).to_csv(output, index=False)


def sample_revisions(article, offset):
    """Sample the revisions for an article at a given offset."""
    title = article.article
    revisions = get_revisions(title)

    revisions.set_index('timestamp', inplace=True)
    sample = revisions.resample(offset).last()

    # Fill missing revids for years w/o edits with the previous year's revid
    sample['revid'] = sample.revid.fillna(method='bfill').astype(int)

    # Drop this year's edits
    last_valid_edit_date = '{}-12-31'.format(CURRENT_YEAR-1)
    sample = sample.ix[:last_valid_edit_date]

    sample.reset_index(inplace=True)
    sample.insert(0, 'article', title)
    return sample


def get_revisions(title):
    """Get all of the revisions for an article."""
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    # hack to turn pywikibot Revisions into records for pandas
    revision_list = [revision.__dict__ for revision in page.revisions()]
    revisions = pandas.DataFrame.from_records(revision_list)
    return revisions
