import os
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: an SQLite CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():

    database = f'{os.getcwd()}{os.sep}db{os.sep}listings.db'

    sql_create_listings_table = """ CREATE TABLE IF NOT EXISTS listings (
                                          id integer PRIMARY KEY,
                                          listing_id integer NOT NULL,
                                          listing_name text NOT NULL,
                                          location text NOT NULL,
                                          cost_per_month integer NOT NULL,
                                          seen_at text NOT NULL
                                      ); """
    sql_create_current_listings_table = """ CREATE TABLE IF NOT EXISTS current_listings (
                                                id integer PRIMARY KEY,
                                                listing_name text NOT NULL
                                            ); """
    sql_create_listings_durations_table = """ CREATE TABLE IF NOT EXISTS listing_durations (
                                                  id integer PRIMARY KEY,
                                                  created_at text NOT NULL,
                                                  removed_at text NOT NULL
                                              ); """
    sql_table_statements = [sql_create_daily_data_table,
                            sql_create_current_listings_table,
                            sql_create_listings_durations_table]

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        for sql_table_statement in sql_table_statements:
            create_table(conn, sql_table_statement)
    else:
        print('Error! Cannot create the database connection.')


if __name__ == '__main__':
    main()