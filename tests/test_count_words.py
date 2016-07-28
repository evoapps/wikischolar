import pytest
import pandas

import wikischolar

def test_count_words():
    revisions = pandas.DataFrame({
        'text': ['one two three', 'one two three four'],
    })

    counts = wikischolar.text.count_words(revisions, id_cols=None)
    assert all(counts.num_words == [3, 4])
