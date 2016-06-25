import sqlite3

import pytest
import pandas

import tasks as wikischolar


def test_count_single_generation():
    revisions = pandas.DataFrame({
        'text': ['aaa', 'bbb', 'aaa', 'ccc'],
        'revid': [1, 2, 3, 4],
        'timestamp': pandas.date_range('2000-01-01', '2000-01-04', freq='D'),
        'title': 'Reverted Article',
    })
    counts = wikischolar.generations.count_generations(revisions)
    assert len(counts) == 2
    assert all(counts.text == ['aaa', 'ccc'])
