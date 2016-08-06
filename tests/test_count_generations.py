import sqlite3

import pytest
import pandas

import wikischolar


def test_count_single_generation():
    revisions = pandas.DataFrame({
        'text': ['aaa', 'bbb', 'aaa', 'ccc'],
        'revid': [1, 2, 3, 4],
        'title': 'Reverted Article',
    })
    counts = wikischolar.plugins.generations.count_generations(revisions)
    assert len(counts) == 2
