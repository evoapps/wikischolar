import functools

import pandas
import pywikibot

from .util import get_revisions

def count_yearly_generations(articles):
    """Count the generations of edits excluding reversions.

    Args:
        articles (pandas.DataFrame): A table of articles with titles.
    Returns:
        A pandas.DataFrame of generations of edits for each year of an
        article's existence.
    """
    offset = pandas.tseries.offsets.YearEnd()
    count_generations_yearly = functools.partial(count_generations,
                                                 offset=offset)
    results = map(count_generations_yearly, articles.itertuples())
    return pandas.concat(results)


def count_generations(article, offset):
    title = article.title
    try:
        revisions = get_revisions(title, content=True)
    except pywikibot.NoPage:
        msg = 'counting generations: revisions for page {} not found'
        logger.debug(msg)
        return pandas.DataFrame()

    # Sort revisions by ascending timestamp
    revisions.set_index('timestamp', inplace=True)
    revisions.sort_index(ascending=True, inplace=True)

    # Count generations (unique revisions)
    generations = revisions.drop_duplicates(subset=['text'], keep='first')
    generations = generations.resample(offset).count()

    # Format output
    generations.reset_index(inplace=True)

    return generations
