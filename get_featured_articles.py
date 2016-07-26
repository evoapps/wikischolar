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
featured['title'] = (featured.line
                             .str.extract(re_title, expand=False)
                             .str.split('|')
                             .str.get(0))

# Select all rows with title and category
featured = featured[['category', 'title']].dropna()

# Select a sample of 1000 articles
featured1000 = featured.sample(1000, random_state=823)
featured1000.to_csv('data/featured/articles.csv', index=False)
