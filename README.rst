wikischolar
===========

This research project provides tools for looking up historical article quality
data for Wikipedia articles using the Wikimedia Foundations Objective Revision
Evaluation Service (ORES)
<https://meta.wikimedia.org/wiki/Objective_Revision_Evaluation_Service>.

    $ git clone git@github.com:evoapps/wikischolar && cd wikischolar
    $ pip install -r requirements.txt
    $ pip install -e .
    $ sch --list  # list available tasks

    load          Populate a new wikischolar database with articles to study.
    dump          Dump a table of the (local) wikischolar database.
    revisions     Get all versions of articles and save them in a local db.
    edits         Tally the number of yearly edits from a list of articles.
    generations   Count the number of generations (edits excluding reversions).
    qualities     Filter a subset of revisions and save the results in a new
                  table.
    execute       Execute a command on the wikischolar db.

Basic usage
-----------

To use wikischolar, you can load articles one at a time, but more likely
you'll want to load a list of articles.

    $ sch load "Splendid fairywren"
    $ sch load data/articles.csv

This creates a sqlite database called "wikischolar.sqlite" in the current
directory with a table called "revisions" containing all revisions to
the articles. To specify a custom database location, add the ``--database`` option.

    $ sch revisions data/articles.csv -d data/wikischolar.sqlite

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
db with the following command chain:

    $ sch load data/articles.csv revisions edits qualities generations

1000 random articles
--------------------

Get historical article quality data for 1000 random articles. This project is a
collaboration with Smallbones
<https://en.wikipedia.org/wiki/User:Smallbones>.
