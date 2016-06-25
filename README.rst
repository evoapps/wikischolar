wikischolar
===========

This research project provides tools for looking up historical article quality
data for Wikipedia articles using the Wikimedia Foundations Objective Revision
Evaluation Service (ORES)
<https://meta.wikimedia.org/wiki/Objective_Revision_Evaluation_Service>.

To install and use the wikischolar tool, clone the repo and install the
required python packages. It is recommended you install these packages
to a virtualenv::

    $ virtualenv --python=python3 ~/.venvs/wikischolar
    $ source ~/.venvs/wikischolar/bin/activate
    (wikischolar) $ cd wikischolar
    (wikischolar) wikischolar/$ pip install -r requirements.txt

The API for wikischolar uses invoke commands that can be issued from the
command line::

    (wikischolar) wikischolar/$ inv --list      # List available commands
    (wikischolar) wikischolar/$ inv -h quality  # Get help on quality command

Basic usage
-----------

To use wikischolar, you create a local library to analyze::
    
    $ inv load data/articles.csv

This creates a sqlite database called "wikischolar.sqlite" in the current
directory with a table called "revisions" containing all revisions to
the articles.

    $ ls | grep *.sqlite
    # wikischolar.sqlite

To specify a custom database location, add the ``--database`` option::

    $ inv revisions data/articles.csv -d data/wikischolar.sqlite

Now you can compute metrics on the particular revisions being studied. For
example, you can calculate the number of edits per year. These results
are saved in a new table in the database called "edits".

    $ inv edits    # assumes wikischolar.sqlite exists in cwd
    $ inv edits -d data/wikischolar.sqlite

You can also obtain the page views for the articles as well::

    $ inv views
 
If multiple invoke commands are chained they will be run in order::

    $ inv load data/articles.csv revisions edits views qualities generations

1000 random articles
--------------------

Get historical article quality data for 1000 random articles. This project is a
collaboration with Smallbones
<https://en.wikipedia.org/wiki/User:Smallbones>.

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

You can also get summaries of yearly edits and page views::

    $ inv yearly_page_views data/1000_random/articles.csv data/1000_random/views.csv
    $ inv count_yearly_edits data/1000_random/articles.csv data/1000_random/edits.csv
