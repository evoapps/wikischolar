import pywikibot
import pandas

def get_revisions(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    # hack to turn pywikibot.Revision into records for pandas
    revision_list = [revision.__dict__ for revision in page.revisions()]
    revisions = pandas.DataFrame.from_records(revision_list)
    return revisions
