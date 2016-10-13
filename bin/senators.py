#!/usr/bin/env python
import sys
from bs4 import BeautifulSoup
import pandas

soup = BeautifulSoup(sys.stdin, 'lxml')
spans = soup.find_all(class_='fn')
names = [sp.find('a').text for sp in spans]
articles = pandas.DataFrame(dict(title=names))
articles.drop_duplicates(inplace=True)
articles.to_csv(sys.stdout, index=False)
