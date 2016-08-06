from concurrent import futures
import functools

import pandas
from numpy import arange
import requests

import wikischolar

# Endpoint to enwiki ORES article quality model
WP10_URL = 'https://ores.wmflabs.org/v2/scores/enwiki/wp10/'

# ORES API throttle
MAX_ORES_THREADS = 4
MAX_ORES_REVIDS = 50

session = requests.Session()


@wikischolar.plugin
def qualities(revisions, offset='YearEnd'):
    """Predict article quality for sampled revisions."""
    offset = wikischolar.parser.get_offset(offset)
    sample = (revisions.set_index('timestamp')
                       .groupby('title')
                       .resample(offset)
                       .last()
                       .revid)
    qualities = wp10_qualities(sample)
    return qualities


def wp10_qualities(revisions):
    """Query the ORES wp10 article quality model for each revision in a table.

    Args:
        revisions (pandas.DataFrame): A table of article revisions with ids.
    Returns:
        A pandas.DataFrame of revisions.
    """
    get_wp10 = functools.partial(get_qualities, endpoint=WP10_URL,
                                 score_formatter=format_wp10_scores)

    chunks = revisions.groupby(arange(len(revisions))//MAX_ORES_REVIDS)
    workers = min(MAX_ORES_THREADS, len(chunks))
    with futures.ThreadPoolExecutor(workers) as executor:
        results = executor.map(get_wp10, chunks)

    qualities_by_revid = pandas.concat(results)
    labeled_qualities = pandas.merge(revisions, qualities_by_revid)
    return labeled_qualities


def get_qualities(articles_group, endpoint, score_formatter):
    _, articles = articles_group
    revids = articles.revid.unique()

    error_msg = 'requesting {} scores when {} is max'
    assert len(revids) <= MAX_ORES_REVIDS,\
        error_msg.format(len(revids), MAX_ORES_REVIDS)

    revids_str = '|'.join(map(str, revids))
    response = session.get(endpoint, params=dict(revids=revids_str))
    return score_formatter(response.json()['scores'])


def format_wp10_scores(scores):
    wp10_scores = scores['enwiki']['wp10']['scores']
    scores = pandas.DataFrame.from_dict(wp10_scores, orient='index')

    scores.index.name = 'revid'
    scores.reset_index(inplace=True)
    scores['revid'] = scores.revid.astype(int)

    scores['prediction'] = unfold(scores.score, 'prediction')
    scores['probabilities'] = unfold(scores.score, 'probability')
    unfold_probs = functools.partial(unfold, objects=scores.probabilities)
    prob_categories = sorted(scores.probabilities.iloc[0].keys())
    for category in prob_categories:
        scores[category] = unfold_probs(name=category)
    del scores['score']
    del scores['probabilities']

    return scores


def unfold(objects, name):
    """Pull the named value out of a Series of dicts."""
    return objects.apply(lambda x: x[name])
