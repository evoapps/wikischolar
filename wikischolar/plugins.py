from invoke import task, Collection

def plugin(func):

    @task(name=func.__name__)
    def func_task(ctx, name=func.__name__, **kwargs):
        return func(*args, **kwargs)

    func_task.__doc__ = func.__doc__

    return func_task


@plugin
def edits(titles):
    """Count the number of edits."""
    print(titles)

@plugin
def words(titles):
    """Count the number of words."""
    print(titles)

namespace = Collection(edits, words)
