from invoke import task

import pywikibot
import requests

@task
def quality():
    """Obtain article quality estimates from the ORES."""
    articles = pandas.read_csv('1000_random.csv')
    articles['ores'] = articles.apply(get_quality, axis=1)


def get_quality(article):
    ores_url = 'https://ores.wmflabs.org/v2/scores/enwiki/wp10/'
    r = requests.get(ores_url, revids=article.revid)
