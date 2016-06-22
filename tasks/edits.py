import pandas


def count_yearly_edits(revisions):
    """Get the yearly edit counts for each article in a table.

    Args:
        revisions (pandas.DataFrame): A table of articles with titles.
    Returns:
        A pandas.DataFrame of edit counts for each year of each article's
        existence.
    """
    offset = pandas.tseries.offsets.YearEnd()
    counts = (revisions.set_index('timestamp')
                       .groupby('title')
                       ['revid']
                       .resample(offset)
                       .count())
    counts.name = 'edits'
    return counts.reset_index()
