import os
import sqlite3
from sqlite3 import Error
import create_database as cdb


def create_listing(conn, listing_values):
    """ insert a new listing row into the listings table, DOES NOT COMMIT
    :param conn: Connection object
    :param listing_values: values to insert to table
    :return: id of inserted listing
    """
    sql_insert_statement = ''' INSERT INTO listings(listing_id, listing_name, location, cost_per_month, seen_at)
                               VALUES(?,?,?,?,?) '''
    c.conn.cursor()
    c.execute(sql_insert_statement, listing_values)
    return c.lastrowid


def main():

    database = f'{os.getcwd()}{os.sep}db{os.sep}listings.db'

    # create a database connection
    conn = cdb.create_connection(database)
    with conn:
        # create a new listing in listings table
        # UPDATE USING DICTIONARY FROM SCRAPING
        # listing = ('','','','','')
        listing_id = create_listing(conn, listing_values)
    # commit inserted listings to database
    conn.commit()

    # closes connection to database
    conn.close()


if __name__ == '__main__':
    main()
