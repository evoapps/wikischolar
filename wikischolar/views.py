from concurrent import futures
import functools
import time

import pandas
import pywikibot
import requests

from .util import get_page

import logging

# Endpoint to wikimedia pageview API
PAGEVIEW_URL = ('https://wikimedia.org/api/rest_v1/'
                'metrics/pageviews/per-article/'
                'en.wikipedia.org/all-access/all-agents/'
                '{title}/daily/{start}/{end}')

TIMEFORMAT = '%Y%m%d'  # e.g., 20160101
TODAY = time.strftime(TIMEFORMAT, time.localtime())

MAX_THREADS = 10


def yearly_page_views(articles):
    """Total the yearly page views for each article.

    Args:
        articles (pandas.DataFrame): A table of articles with titles.
    Returns:
        A pandas.DataFrame of article titles with yearly view totals.
    """
    offset = pandas.tseries.offsets.YearEnd()
    sample_page_views_yearly = functools.partial(sample_page_views, offset=offset)
    workers = min(MAX_THREADS, len(articles))
    with futures.ThreadPoolExecutor(workers) as executor:
        results = executor.map(sample_page_views_yearly, articles.itertuples())
    return pandas.concat(results)


def sample_page_views(article, offset):
    title = article.title
    page = get_page(title)

    try:
        start = page.oldest_revision['timestamp'].strftime(TIMEFORMAT)
    except pywikibot.NoPage:
        msg = 'Page views requested for {} but no page was found'
        print(msg.format(title))
        logging.debug(msg.format(title))
        return pandas.DataFrame()
    else:
        end = TODAY

    try:
        page_views = daily_page_views(title, start, end)
    except KeyError:
        msg = 'Page views requested for {} from {} to {} but not receieved'
        logging.debug(msg.format(title, start, end))
        return pandas.DataFrame()

    page_views['timestamp'] = pandas.to_datetime(page_views.timestamp,
                                                 format=TIMEFORMAT+'00')
    page_views.set_index('timestamp', inplace=True)
    sums = page_views.resample(offset).sum()
    sums.reset_index(inplace=True)
    return sums


def daily_page_views(title, start, end):
    url = PAGEVIEW_URL.format(title=slugify(title), start=start, end=end)
    response = requests.get(url)
    records = response.json()['items']
    pageviews = pandas.DataFrame.from_records(records)
    pageviews.insert(0, 'title', title)
    return pageviews


def slugify(title):
    return title.replace(' ', '_')
