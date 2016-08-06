import pytest
import pandas

import wikischolar


@pytest.mark.usefixtures('betamax_session')
def test_wp10_quality(betamax_session):
    revisions = pandas.DataFrame({'revid': [691949610]})
    qualities = wikischolar.plugins.qualities.wp10_qualities(revisions)
    assert len(qualities) == 1
