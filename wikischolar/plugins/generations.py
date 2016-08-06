import hashlib

import pandas
from mw.lib import reverts

import wikischolar


@wikischolar.plugin
def generations(revisions, offset='YearEnd'):
    offset = wikischolar.parser.get_offset(offset)
    counts = (revisions.set_index('timestamp')
                       .groupby('title')
                       .apply(count_generations)
                       .reset_index(level=0, drop=True)
                       .resample(offset)
                       .count())
    counts.name = 'generations'
    return counts.reset_index()


def count_generations(revisions):
    # assume revisions are ordered in increasing time
    revisions.reset_index(inplace=True)
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
    revisions = revisions.ix[revisions.is_extinct == 0.0]
    revisions.reset_index(drop=True)
    revisions.set_index('timestamp', inplace=True)
    return revisions


def checksum(text=None):
    text = text or ''
    return hashlib.sha1(text.encode('utf-8')).hexdigest()
