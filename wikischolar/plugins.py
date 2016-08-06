from invoke import task, Collection

def plugin(func):

    @task(name=func.__name__)
    def func_task(ctx, *args, **kwargs):
        revisions = checkout()

        return func(*args, **kwargs)

    func_task.__doc__ = func.__doc__

    return func_task


@plugin
def edits(revisions, offset='YearEnd'):
    """Count the number of edits."""
    offset = getattr(pandas.tseries.offsets, offset)()
    counts = (revisions.set_index('timestamp')
                       .groupby('title')
                       ['revid']
                       .resample(offset)
                       .count())
    counts.name = 'edits'
    return counts.reset_index()


@plugin
def words(revisions, offset='YearEnd'):
    """Count the number of words."""

    offset = getattr(pandas.tseries.offsets, offset)()



    db = wikischolar.db.connect(database)
    try:
        sample = wikischolar.revisions.resample_revisions(db, offset)
        counts = wikischolar.text.count_words(sample)
        counts.to_sql('words', db, if_exists='append', index=False)
    finally:
        db.close()


namespace = Collection(checkout)
