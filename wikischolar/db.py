from os import environ
import sqlite3

import pandas
import unipath

DEFAULT_DB_NAME = 'wikischolar.sqlite'

def connect(database=None, must_exist=True):
    """Return a connection to a sqlite database."""
    database = database or environ.get('WIKISCHOLAR_DB') or DEFAULT_DB_NAME
    if must_exist and not unipath.Path(database).exists():
        raise MissingDatabaseException(database)
    return sqlite3.connect(database)


def query(sql_query, db):
    return pandas.read_sql_query(sql_query, db)


class MissingDatabaseException(LookupError):
    """The expected database was not found."""
