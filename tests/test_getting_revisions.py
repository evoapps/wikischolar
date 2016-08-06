import pywikibot
import pytest
import wikischolar


@pytest.mark.usefixtures('betamax_session')
def test_getting_revisions(betamax_session):
    pywikibot.comms.http.session = betamax_session
    revisions = wikischolar.revisions.get_revisions('Splendid fairywren')
    assert 'title' in revisions
