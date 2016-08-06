import pytest
import pandas

import wikischolar

def test_count_words():
    revisions = pandas.DataFrame({
        'text': ['one two three', 'one two three four'],
        'timestamp': pandas.to_datetime(['2015-01-01', '2016-01-02']),
        'title': 'Wordy'
    })

    counts = wikischolar.plugins.words.words(revisions)
    print(counts)
    assert all(counts.words == [3, 4])
