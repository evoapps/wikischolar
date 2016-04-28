from concurrent import futures
import functools

from invoke import task
import pywikibot
import pandas

MAX_WORKERS = 4

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
    # Fill revids for years without edits with the previous year's revid
    sample['revid'] = sample.revid.fillna(method='bfill').astype(int)
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
