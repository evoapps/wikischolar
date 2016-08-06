import pytest
import pandas

import wikischolar

@pytest.mark.usefixtures('betamax_session')
class TestWP10Quality:
    def test_wp10_quality(self, betamax_session):
        revisions = pandas.DataFrame({'revid': [691949610]})
        wikischolar.plugins.qualities.session = betamax_session
        qualities = wikischolar.plugins.qualities.wp10_qualities(revisions)
        assert len(qualities) == 1
