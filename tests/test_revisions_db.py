import sqlite3

import pytest
import pandas

import tasks as wikischolar


@pytest.fixture
def db(request):
    db = sqlite3.connect(':memory:')
    def close_db():
        db.close()
    request.addfinalizer(close_db)
    return db


def test_save_and_load_revisions(db):
    saved = wikischolar.revisions.save_revisions('Splendid fairywren', db)
    loaded = pandas.read_sql_query('SELECT * FROM revisions;', db)
    assert len(saved) == len(loaded)
