from invoke import task

@task
def get(wikilink):
    """Get table of data from the wikilink."""
    print('getting ' + wikilink)

@task
def article_quality(articles_csv):
    """Get the ORES article quality scores."""
    print('getting ores article quality scores from ' + articles_csv)
