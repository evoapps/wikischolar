import wikischolar


@wikischolar.plugin
def words(revisions, offset='YearEnd'):
    offset = wikischolar.parser.get_offset(offset)
    sample = (revisions.set_index('timestamp')
                       .groupby('title')
                       .resample(offset)
                       .last()
                       .text
                       .str.split()
                       .apply(len))
    sample.name = 'words'
    return sample.reset_index()
