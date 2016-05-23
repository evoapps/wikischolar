from concurrent import futures
import functools

from invoke import task

import pandas

from .util import get_revisions

MAX_WORKERS = 4


@task(aliases=['edits'])
def count_yearly_edits(articles, output):
    """Get yearly edit counts for each article."""
    articles = pandas.read_csv(articles)

    offset = pandas.tseries.offsets.YearEnd()
    count_edits_yearly = functools.partial(count_edits, offset=offset)
    workers = min(MAX_WORKERS, len(articles))

    with futures.ThreadPoolExecutor(workers) as executor:
        results = executor.map(count_edits_yearly, articles.itertuples())
    pandas.concat(results).to_csv(output, index=False)


def count_edits(article, offset):
    """Count the number of revisions for an article in a given timespan."""
    title = article.title
    revisions = get_revisions(title)

    revisions.set_index('timestamp', inplace=True)
    edits = revisions.resample(offset).count()

    edits.reset_index(inplace=True)
    edits.insert(0, 'title', title)
    return edits
