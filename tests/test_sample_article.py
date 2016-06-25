"""Test wikischolar commands for a sample article.

Warning! These tests are run live against the Wikipedia servers.
TODO: Swap out real requests with betamaxx
"""
import pytest
import pandas

import tasks as wikischolar


@pytest.fixture
def revisions():
    return pandas.DataFrame({'revid': [691949610]})

def test_getting_revisions():
    revisions = wikischolar.revisions.get_revisions('Splendid fairywren')
    assert 'title' in revisions

def test_wp10_quality(revisions):
    qualities = wikischolar.quality.wp10_qualities(revisions)
    assert len(qualities) == 1
