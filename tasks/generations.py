import functools

import pandas
import pywikibot

def count_yearly_generations(revisions):
    """Count the generations of edits excluding reversions.

    Args:
        revisions (pandas.DataFrame): A table of revisions.
    Returns:
        A pandas.DataFrame of generations of edits for each year of an
        article's existence.
    """
    offset = pandas.tseries.offsets.YearEnd()
    generations = (revisions.set_index('timestamp')
                            .groupby('title')
                            .resample(offset)
                            .apply(count_generations))

    assert False, 'TODO'

    count_generations_yearly = functools.partial(count_generations,
                                                 offset=offset)
    results = map(count_generations_yearly, articles.itertuples())
    return pandas.concat(results)


def count_generations(revisions):
    revisions['generations'] = 1
    return revisions
