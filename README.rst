wikischolar
===========

This research project provides tools for looking up historical article quality
data for Wikipedia articles using the Wikimedia Foundations Objective Revision
Evaluation Service (ORES)
<https://meta.wikimedia.org/wiki/Objective_Revision_Evaluation_Service>.

Clone and install (recommended)
-------------------------------

The recommended installation method is to clone the repo and use pip
to install it in editable form::

    $ git clone git@github.com:evoapps/wikischolar && cd wikischolar
    $ pip install -r requirements.txt
    $ pip install -e .
    # sch -l  # list available tasks

Install from github
-------------------

Alternatively you can try to install directly from github with pip::

    $ pip install git+git://github.com/evoapps/wikischolar.git#egg=wikischolar
    $ sch -l

Basic usage
-----------

To use wikischolar, you can load articles one at a time, but more likely
you'll want to load a list of articles::

    $ sch load "Splendid fairywren"
    $ sch load data/articles.csv
    # creates ./wikischolar.sqlite

This creates a sqlite database called "wikischolar.sqlite" in the current
directory with a table called "articles" containing all the articles that
you want to study. To specify a custom database location, add the
``--database`` option, or set the WIKISCHOLAR_DB environment variable::

    $ sch revisions data/articles.csv -d data/wikischolar.sqlite
    # or
    $ export WIKISCHOLAR_DB=data/wikischolar.sqlite
    $ sch revisions data/articles.csv

The next step is to download the revisions for the articles that you
want to study. Do this with the **revisions** command. By default,
**revisions** gets the revisions for all articles in the "articles"
table, and puts them in a table called "revisions". These options
can be modified to create different tables::

    $ sch revisions

**Be careful**. I sampled 1000 random Featured Articles and the full text
revisions was about 40gb, and it was not fun to work with. Although it
would be possible to swap out the database for anything supported by
SQLAlchemy, it's not worth the effort at this point, as there are much
better solutions than this already out there, and much faster ways to get
article revisions than querying the live servers.

Now you can compute metrics on the particular revisions being studied. For
example, you can calculate the number of edits per year. These results
are saved in a new table in the database called "edits". You can also get
the number of generations (edits minus reversions) and yearly quality
predictions from the ORES API. If multiple wikischolar commands are chained
they will be run in order. You can get a fully populated wikischolar
db with the following command chain::

    $ sch load data/articles.csv revisions edits qualities generations

Qualities
---------

Qualities are downloaded via the ORES API which provides quality estimates
based on Wikipedia article revids. This may get tedious for moderate samples
of articles. Luckily, the WMF has made a sqlite database containing all
article quality estimates available for download.

**Warning** the entire db of article quality estimates is about 40gb.
Before this data is downloaded, a quick check of the available space
is done, but be aware of any space constraints on your machine.

    $ sch download_bulk_articles -d data/bulk_qualities.sqlite

1000 random articles
--------------------

Get historical article quality data for 1000 random articles. This project is a
collaboration with Smallbones
<https://en.wikipedia.org/wiki/User:Smallbones>.
