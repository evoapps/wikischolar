PLUGINS = {}

def plugin(func):
    """Decorator for plugins. Saves results to a database."""
    table = func.__name__
    def save(*args, database=None, **kwargs):
        try:
            results = func(*args, **kwargs)
        except Exception as err:
            msg = 'Error in {} plugin: {}'
            raise PluginError(msg.format(table, err))
        else:
            results.to_sql(table, results, if_exists='append', index=False)
    PLUGINS[table] = save
    return save


class PluginError(RuntimeError):
    """Something happened with this plugin."""
