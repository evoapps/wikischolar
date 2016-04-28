wikischolar
===========

Look up historical article quality data for Wikipedia articles.

1000 random articles
--------------------

First, get the list of articles to research. To get the articles
from a mediawiki table, use the ``get_table`` command::

    $ inv get_table User:Smallbones/1000_random --output=data/1000_random/articles.csv

Otherwise, a list of articles can be created by hand. All that is necessary for
the remaining steps is that in the csv of articles there is a column named
"article" holding the titles of the articles.

With the article titles in hand, the next step is to get the revision ids for
versions of articles at the end of each year since they were created. This is
done using the ``fill_ids`` and specifying a period to sample::

    $ inv fill_yearly_ids data/1000_random/articles.csv --output=data/1000_random/revisions.csv

The output of this command is similar to the input, but instead of each
article occupying a single row, the table has been expanded so that there
are multiple rows for each article, one row for the article at each sampled
time bin.

Finally, we can get the ORES scores for each of the revisions
with the ``quality`` command::

    $ inv wp10_quality data/1000_random/revisions.csv --output=data/1000_random/qualities.csv
