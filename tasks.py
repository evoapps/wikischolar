from invoke import task, run, Collection
import unipath

import wikischolar

@task
def export(ctx):
    """Dump tables from wikischolar.sqlite and save the in wikischolarlib."""
    tables = ['articles', 'qualities', 'edits', 'generations']
    out = lambda x: unipath.Path('wikischolarlib/data-raw/{}.csv'.format(x))
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
