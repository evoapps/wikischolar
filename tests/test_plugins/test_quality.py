import pytest
import pandas

import wikischolar


@pytest.mark.usefixtures('betamax_session')
def test_wp10_quality(betamax_session):
    revisions = pandas.DataFrame({'revid': [691949610]})
    wikischolar.plugins.qualities.session = betamax_session
    qualities = wikischolar.plugins.qualities.wp10_qualities(revisions)
    assert len(qualities) == 1
