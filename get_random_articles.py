#!/usr/bin/env python
import sys
import wikischolar
import pandas

table = wikischolar.get.get_table('User:Smallbones/1000_random')
articles = table[['title']]
articles.to_csv(sys.stdout, index=False)
