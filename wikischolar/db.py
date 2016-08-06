from os import environ
import sqlite3

import pandas
import unipath

DB_NAME = 'wikischolar.sqlite'


def connect(database, must_exist=True):
    """Return a connection to a sqlite database.

    Args:
        database (str): Optional. The name of the sqlite database to connect
            to. Defaults to `wikischolar.sqlite` in the current directory.
            Can also be set with the environment variable `WIKISCHOLAR_DB`.
        must_exist (bool): Optional. Defaults to True. Whether or not the
            connection should fail if the database is not found.
    """
    db_loc = unipath.Path(database or environ.get('WIKISCHOLAR_DB') or DB_NAME)
    if must_exist and not db_loc.exists():
        raise MissingDatabaseException(db_loc)
    return sqlite3.connect(db_loc)


def query(sql_query, db):
    return pandas.read_sql_query(sql_query, db)


class MissingDatabaseException(LookupError):
    """The expected database was not found."""
