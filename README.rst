wikischolar
===========

Look up historical article quality data for Wikipedia articles.

1000 random articles
--------------------

First, get the list of articles to research. To get the articles
from a mediawiki table, use the ``get_table`` command::

    $ inv get_table User:Smallbones/1000_random --output=data/1000_random/articles.csv

The next step is to get the revision ids for versions of articles
at the end of each year since they were created. This is done
using the ``fill_ids`` and specifying a period to sample::

    $ inv fill_ids data/1000_random/articles.csv --period=yearly --output=data/1000_random/revisions.csv

Finally, we can get the ORES scores for each of the revisions
with the ``quality`` command::

    $ inv quality data/1000_random/revisions.csv --output=data/1000_random/qualities.csv
