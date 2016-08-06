import pytest
import pandas

import wikischolar


@pytest.fixture
def revisions():
    return pandas.DataFrame({'revid': [691949610]})

@pytest.mark.usefixtures('betamax_session', 'revisions')
class TestWP10Quality:
    def test_wp10_quality(self, betamax_session, revisions):
        wikischolar.plugins.qualities.session = betamax_session
        qualities = wikischolar.plugins.qualities.wp10_qualities(revisions)
        assert len(qualities) == 1

    def test_qualities(self, betamax_session, revisions):
        pass
