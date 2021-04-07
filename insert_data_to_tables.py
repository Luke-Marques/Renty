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


def create_listing(conn, listing)
    """ insert a new listing row into the listings table, DOES NOT COMMIT
    :param conn: Connection object
    :param listing: values to insert to table
    :return: id of inserted listing
    """
    sql_insert_statement = ''' INSERT INTO listings(listing_id, listing_name, location, cost_per_month, seen_at)
                               VALUES(?,?,?,?,?) '''
    c.conn.cursor()
    c.execute(sql_insert_statement, listing)
    return c.lastrowid


def main():

    database = f'{os.getcwd()}{os.sep}db{os.sep}listings.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new listing in listings table
        # UPDATE USING DICTIONARY FROM SCRAPING
        # listing = ('','','','','')
        listing_id = create_listing(conn, listing)
    # commit inserted listings to database
    conn.commit()

if __name__ == '__main__':
    main()