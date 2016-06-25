import pandas

def count_yearly_edits(revisions, name='edits'):
    """Get the yearly edit counts for each article in a table of revisions.

    Args:
        revisions (pandas.DataFrame): A table of revisions.
        name (str): The name of the count column in the resulting DataFrame.
            Default is 'edits'. Useful when counting subsets of edits, like
            generations or edits from a particular user.
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
    counts.name = name
    return counts.reset_index()
