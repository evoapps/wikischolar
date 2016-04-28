from invoke import task, run

R_PKG_NAME = 'wikischolarlib'


@task
def data():
    """Run the use-data.R script to compile raw data into .rda files."""
    cmd = "cd {} && Rscript data-raw/use-data.R"
    run(cmd.format(R_PKG_NAME))


@task
def install():
    """Install the wikischolarlib R package."""
    r_commands = [
        'devtools::document("{}")'.format(R_PKG_NAME),
        'devtools::install("{}")'.format(R_PKG_NAME),
    ]
    for r_command in r_commands:
        run("Rscript -e '{}'".format(r_command))
