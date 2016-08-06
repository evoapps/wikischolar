import wikischolar


@wikischolar.plugin
def edits(revisions, offset='YearEnd'):
    """Count the number of edits."""
    offset = wikischolar.parser.get_offset(offset)
    counts = (revisions.set_index('timestamp')
                       .groupby('title')
                       .revid
                       .resample(offset)
                       .count())
    counts.name = 'edits'
    return counts.reset_index()
