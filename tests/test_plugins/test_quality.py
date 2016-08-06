import sqlite3

import pytest
import pandas
import pywikibot

import wikischolar


@pytest.fixture
def revisions():
    return pandas.DataFrame({
        'title': 'Splendid fairywren',
        'revid': [691949610],
        'timestamp': pandas.to_datetime('2015-01-01'),
    })

@pytest.mark.usefixtures('betamax_session', 'revisions')
class TestWP10Quality:
    def test_wp10_quality(self, betamax_session, revisions):
        wikischolar.plugins.qualities.session = betamax_session
        qualities = wikischolar.plugins.qualities.wp10_qualities(revisions)
        assert len(qualities) == 1
        assert 'title' in qualities

    def test_qualities(self, betamax_session, revisions):
        wikischolar.plugins.qualities.session = betamax_session
        qualities = wikischolar.plugins.qualities.qualities(revisions)
        assert len(qualities) == 1

    def test_write_qualities_to_db(self, betamax_session, revisions):
        wikischolar.plugins.qualities.session = betamax_session
        database = sqlite3.connect(':memory:')
        qualities = wikischolar.plugins.qualities.qualities(
            revisions, database=database,
        )
        retrieved = wikischolar.db.query('SELECT * FROM qualities', database)
        assert all(qualities.prediction == retrieved.prediction)

    def test_missing_qualities(self, betamax_session):
        pywikibot.comms.http.session = betamax_session
        revisions = wikischolar.revisions.get_revisions('Major Lance')

        wikischolar.plugins.qualities.session = betamax_session
        qualities = wikischolar.plugins.qualities.qualities(revisions)

    def test_write_missing_qualities_to_db(self, betamax_session):
        pywikibot.comms.http.session = betamax_session
        revisions = wikischolar.revisions.get_revisions('Major Lance')

        wikischolar.plugins.qualities.session = betamax_session
        database = sqlite3.connect(':memory:')
        qualities = wikischolar.plugins.qualities.qualities(
            revisions, database=database,
        )
        retrieved = wikischolar.db.query('SELECT * FROM qualities', database)
        assert all(qualities.prediction == retrieved.prediction)
