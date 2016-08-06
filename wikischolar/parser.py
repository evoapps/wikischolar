import pandas
import wikischolar


def get_offset(offset):
    return getattr(pandas.tseries.offsets, offset)()


def load_plugins(names):
    plugins = []
    for name in names:
        try:
            plugin = wikischolar.plugins.PLUGINS[name]
        except KeyError:
            msg = 'plugin "{}" not found'
            raise wikischolar.plugins.PluginError(msg.format(name))
        else:
            plugins.append(plugin)
    return plugins


def load_revisions(titles):
    for title in titles:
        yield wikischolar.revisions.get_revisions(title, content=True)


def load_articles(articles):
    return pandas.read_csv(articles)
