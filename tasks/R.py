from invoke import task, run
import unipath

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


@task
def reports():
    """Compile knitr reports."""
    proj_root = unipath.Path(__file__).absolute().ancestor(2)
    reports = unipath.Path(proj_root, 'reports')

    cmd = 'rmarkdown::render("{}")'
    for rmd in reports.walk(filter=lambda x: unipath.Path(x).ext == '.Rmd'):
        rmd_cmd = cmd.format(rmd)
        run("Rscript -e '{}'".format(rmd_cmd))
