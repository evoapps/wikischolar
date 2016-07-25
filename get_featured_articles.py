#!/usr/bin/env python
import pandas
import wikischolar

wiki_text = wikischolar.get_wiki('Wikipedia:Featured_articles')
featured = pandas.DataFrame({'line': wiki_text.splitlines()})

# Extract section headers
re_section = r'^==([^=]+)==$'
featured['category'] = (featured.line
                                .str.extract(re_section, expand=False)
                                .ffill())

# Extract title
re_title = r'^\*.+\[\[(.+)\]\]'
featured['title'] = featured.line.str.extract(re_title, expand=False)

# Select all rows with title and category
featured = featured[['category', 'title']].dropna()
featured.to_csv('data/featured/Featured_articles.csv', index=False)
