from concurrent import futures
import functools

from invoke import task
import pywikibot
import pandas
from numpy import arange
import requests

# Endpoint to enwiki ORES article quality model
WP10_URL = 'https://ores.wmflabs.org/v2/scores/enwiki/wp10/'

# ORES API throttle
MAX_ORES_THREADS = 4
MAX_ORES_REVIDS = 50


@task(aliases=['quality'])
def wp10_quality(revisions, output):
    """Obtain article quality estimates from the ORES."""
    unassessed = pandas.read_csv(revisions)
    get_wp10 = functools.partial(get_qualities, endpoint=WP10_URL,
                                 score_formatter=format_wp10_scores)

    chunks = unassessed.groupby(arange(len(unassessed))//MAX_ORES_REVIDS)
    workers = min(MAX_ORES_THREADS, len(chunks))
    with futures.ThreadPoolExecutor(workers) as executor:
        qualities = executor.map(get_wp10, chunks)

    quality = pandas.concat(qualities)
    assessed = unassessed.merge(quality)
    assessed.to_csv(output, index=False)


def get_qualities(articles_group, endpoint, score_formatter):
    _, articles = articles_group
    revids = articles.revid.unique()

    error_msg = 'requesting {} scores when {} is max'.format(
        len(revids), MAX_ORES_REVIDS)
    assert len(revids) <= MAX_ORES_REVIDS, error_msg

    revids_str = '|'.join(map(str, revids))
    response = requests.get(endpoint, params=dict(revids=revids_str))
    return score_formatter(response.json()['scores'])


def format_wp10_scores(response_json):
    score_dicts = response_json['enwiki']['wp10']['scores']
    scores = pandas.DataFrame.from_dict(score_dicts, orient='index')
    scores.index.name = 'revid'
    scores.reset_index(inplace=True)
    scores['revid'] = scores.revid.astype(int)

    unfold_probs = functools.partial(unfold, objects=scores.probability)
    prob_categories = sorted(scores.probability.iloc[0].keys())
    for category in prob_categories:
        scores[category] = unfold_probs(name=category)
    del scores['probability']

    return scores


def unfold(objects, name):
    """Pull the named value out of a Series of objects."""
    return objects.apply(lambda x: x[name])
