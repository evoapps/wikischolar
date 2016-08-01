import sqlite3
import pytest
import wikischolar

@pytest.fixture
def db(request):
    db = sqlite3.connect(':memory:')
    wikischolar.revisions.save_revisions('Splendid fairywren', db)
    def close_db():
        db.close()
    request.addfinalizer(close_db)
    return db


def test_checkout_columns(db):
    selected_columns = 'title'
    revisions = wikischolar.revisions.checkout_all_revisions(db,
                                                             selected_columns)
    assert all(revisions.columns == selected_columns)
