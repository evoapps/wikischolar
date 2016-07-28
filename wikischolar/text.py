"""Analytics of Wikipedia article text."""

def count_words(revisions, id_cols=['title', 'revid']):
    if not id_cols:
        id_cols = revisions.columns
    counted = revisions[id_cols]
    counted['num_words'] = revisions.text.str.split().apply(len)
    return counted
