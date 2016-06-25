import sqlite3

import unipath

DB_NAME = 'wikischolar.sqlite'

def connect(database, must_exist=True):
    """Return a connection to a sqlite database."""
    db_loc = unipath.Path(database or DB_NAME)
    if must_exist and not db_loc.exists():
        raise MissingDatabaseException(db_loc)
    return sqlite3.connect(db_loc)


def query(sql_query, db):
    return pandas.read_sql_query(sql_query, db)


class MissingDatabaseException(LookupError):
    """The expected database was not found."""
