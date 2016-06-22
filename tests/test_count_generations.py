import sqlite3

import pytest
import pandas

import tasks as wikischolar


def test_count_single_generation():
    revisions = pandas.DataFrame({
        'timestamp': ['2015-01-01'],
        'content': ['hello!'],
    })
    counts = wikischolar.generations.count_generations(revisions)
    assert len(counts) == 1
    assert counts.generations.iloc[0] == 1
