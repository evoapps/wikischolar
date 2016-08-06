import pytest
import pandas

import wikischolar


@pytest.fixture
def revisions():
    return pandas.DataFrame({'revid': [691949610]})


def test_wp10_quality(revisions):
    qualities = wikischolar.plugins.qualities.wp10_qualities(revisions)
    assert len(qualities) == 1
