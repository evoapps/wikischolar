from invoke import task

import pywikibot
import pandas


@task
def fill_ids(articles, period, output):
    """Retrieve the revision ids for each article sampled periodically."""
    if period == 'yearly':
        offset = pandas.tseries.offsets.YearEnd()
    else:
        raise NotImplementedError

    articles = pandas.read_csv(articles)
    revisions = []
    for _, article in articles.iterrows():
        article_revisions = get_revision_ids(article, offset)
        revisions.append(article_revisions)
    revisions = pandas.concat(revisions)
    revisions.to_csv(output, index=False)


def get_revision_ids(article, offset):
    title = article.article
    revisions = get_revisions(title)
    revisions.set_index('timestamp', inplace=True)
    sample = revisions.resample(offset).last()
    sample.reset_index(inplace=True)
    sample.insert(0, 'article', title)
    return sample


def get_revisions(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    # hack to turn pywikibot.Revision into records for pandas
    revision_list = [revision.__dict__ for revision in page.revisions()]
    revisions = pandas.DataFrame.from_records(revision_list)
    return revisions
