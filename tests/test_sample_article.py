"""Test wikischolar commands for a sample article.

Warning! These tests are run live against the Wikipedia servers.
"""
import pytest
import pandas

import tasks as wikischolar


@pytest.fixture
def articles():
    return pandas.DataFrame({'title': ['Splendid fairywren']})

@pytest.fixture
def revisions():
    return pandas.DataFrame({'revid': [691949610]})

def test_yearly_ids(articles):
    revids = wikischolar.fill.fill_yearly_ids(articles)
    assert len(revids) > 0

def test_yearly_edits(articles):
    edits = wikischolar.edits.count_yearly_edits(articles)
    assert len(edits) > 0

def test_wp10_quality(revisions):
    qualities = wikischolar.quality.wp10_qualities(revisions)
    assert len(qualities) == 1

def test_missing_article(articles):
    missing = pandas.DataFrame({'title': ['not-a-real-article']})
    edits = wikischolar.edits.count_yearly_edits(missing)
    revids = wikischolar.fill.fill_yearly_ids(missing)
    views = wikischolar.views.yearly_page_views(missing)
    assert len(edits) == len(revids) == len(views) == 0

def test_missing_page_views():
    no_page_views = wikischolar.util.read('Tinie Tempah', is_value=True,
                                          name='title')
    wikischolar.views.yearly_page_views(no_page_views)
