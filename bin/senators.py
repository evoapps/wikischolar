#!/usr/bin/env python
import sys
from bs4 import BeautifulSoup
import pandas
import wikischolar

title = "List of current United States senators"
html = wikischolar.util.get_page_html(title)
soup = BeautifulSoup(html, 'lxml')
spans = soup.find_all(class_='fn')
names = [sp.find('a').text for sp in spans]
articles = pandas.DataFrame(dict(title=names))
articles.drop_duplicates(inplace=True)
articles.to_csv(sys.stdout, index=False)
