import pandas

def load_offset(offset):
    return getattr(pandas.tseries.offsets, offset)()


def load_plugins(names):
    plugins = []
    for name in names:
        try:
            plugin = getattr(wikischolar.plugins, name)
        except AttributeError:
            raise AttributeError('plugin "{}" not found'.format(name))
        else:
            plugins.append(plugin)
    return plugins


def load_revisions(titles):
    for title in titles:
        yield wikischolar.revisions.get_revisions(title, content=True)
