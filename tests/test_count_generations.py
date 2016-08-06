import sqlite3

import pytest
import pandas

import wikischolar


def test_count_single_generation():
    revisions = pandas.DataFrame({
        'text': ['aaa', 'bbb', 'aaa', 'ccc'],
        'revid': [1, 2, 3, 4],
        'title': 'Reverted Article',
        'timestamp': pandas.to_datetime(['2015-01-01', '2015-01-02']),
    })
    counts = wikischolar.plugins.generations.count_generations(revisions)
    assert len(counts) == 2
