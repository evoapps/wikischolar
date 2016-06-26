import functools
import hashlib

import pandas
import pywikibot
from mw.lib import reverts

from wikischolar.edits import count_yearly_edits

def count_yearly_generations(revisions):
    """Count the generations of edits excluding reversions.

    Args:
        revisions (pandas.DataFrame): A table of revisions.
    Returns:
        A pandas.DataFrame of generations of edits for each year of an
        article's existence.
    """
    offset = pandas.tseries.offsets.YearEnd()
    generations = (revisions.groupby('title')
                            .apply(count_generations))

    return generations


def count_generations(revisions):
    # assume revisions are ordered in increasing time
    revisions.set_index(revisions.text.apply(checksum), inplace=True)
    parsed = reverts.detect(revisions.iterrows())

    rev_map = pandas.Series(index=revisions.revid, name='is_extinct')
    for (rev, rev_eds, rev_to) in parsed:
        # drop reversion and edits that were reverted
        revs_to_drop = [rev['revid']] + [r['revid'] for r in rev_eds]
        rev_map.loc[revs_to_drop] = 1.0
        rev_map.loc[rev_to['revid']] = 0.0
    rev_map.fillna(0.0, inplace=True)  # keep everything else
    rev_map = rev_map.reset_index()

    revisions = revisions.merge(rev_map)
    generations = count_yearly_edits(revisions.ix[revisions.is_extinct == 0.0],
                                     name='generations')

    return generations


def checksum(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()
