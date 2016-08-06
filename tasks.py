import sys

import unipath
import pandas
from invoke import task, run, Collection

import wikischolar

@task
def export(ctx, name):
    """Dump tables from wikischolar db and save in wikischolarlib.

    Args:
        name (str): The name to associate with the data.
    """
    tables = ['articles', 'qualities', 'edits', 'generations']
    out = lambda x: \
        unipath.Path('wikischolarlib/data-raw/{}/{}.csv'.format(name, x))
    for table in tables:
        wikischolar.tasks.dump(ctx, table, output=out(table))

@task
def use_data(ctx):
    """Run the use-data script to convert csv to rda files."""
    run('cd wikischolarlib && Rscript data-raw/use-data.R')


@task
def install(ctx):
    """Install the wikischolarlib R package."""
    # watch quotes!
    commands = [
        "devtools::document('wikischolarlib')",
        "devtools::install('wikischolarlib')",
    ]
    for cmd in commands:
        run('Rscript -e "{}"'.format(cmd))


@task
def get_featured_articles(ctx):
    """Download 1000 random featured articles."""
    wiki_text = wikischolar.util.get_wiki('Wikipedia:Featured_articles')
    featured = pandas.DataFrame({'line': wiki_text.splitlines()})

    # Extract section headers
    re_section = r'^==([^=]+)==$'
    featured['category'] = (featured.line
                                    .str.extract(re_section, expand=False)
                                    .ffill())

    # Extract title
    re_title = r'^\*.+\[\[(.+)\]\]'
    featured['title'] = (featured.line
                                 .str.extract(re_title, expand=False)
                                 .str.split('|')
                                 .str.get(0))

    # Select all rows with title and category
    featured = featured[['category', 'title']].dropna()

    # Select a sample of 1000 articles
    featured1000 = featured.sample(1000, random_state=823)
    featured1000.to_csv(sys.stdout, index=False)


@task
def get_random_articles(ctx):
    """Download User:Smallbones 1000 random articles."""
    table = wikischolar.util.get_table('User:Smallbones/1000_random')
    articles = table[['title']]
    articles.to_csv(sys.stdout, index=False)


@task
def clean(ctx):
    trash = '.cache/ throttle.ctrl apicache/'
    run('rm -rf {}'.format(trash))
