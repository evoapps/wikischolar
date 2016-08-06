Plugins
=======

Wikischolar provides a number of plugins for processing individual Wikipedia articles.

edits
: Tally the number of edits in a given timespan, e.g., yearly.

generations
: Keep track of edits and reversions and count the number of generations in a given timespan, e.g., yearly.

qualities
: Use the `wp10` machine learning algorithm to calculate article quality sampled at a given increment, e.g., year end.

Plugins are meant to be piped together.

Custom plugins
--------------

You can provide custom plugins if they implement the basic interface of accepting a `pandas.DataFrame` of revisions for an article and outputting a `pandas.DataFrame` of results. For instance, here is the implementation of the `words` plugin.

.. code-block:: python

    @wikischolar.plugin
    def words(revisions):
        """Count the number of times a word was used in an article."""
        # ...
        return words
