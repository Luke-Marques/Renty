import os
import sqlite3
from sqlite3 import Error


def create_db_dir(path_to_dir):
    """ create new directory to store sqlite3 database file
    :param path_to_dir: absolute path for new database directory
    :return:
    """
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)


def create_connection(db_file):
    """ create a database connection to SQLite database specified by db_file, will make database if does not db_file
    does not already exist
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
    create_db_dir(f'{os.getcwd()}{os.sep}db')

    database = f'{os.getcwd()}{os.sep}db{os.sep}properties.db'

    sql_create_properties_table = ''' CREATE TABLE IF NOT EXISTS properties (
                                        id integer PRIMARY KEY,
                                        property_id integer NOT NULL,
                                        address text NOT NULL,
                                        location text NOT NULL,
                                        price integer NOT NULL,
                                        seen_at text NOT NULL
                                      ); '''
    sql_create_current_properties_table = ''' CREATE TABLE IF NOT EXISTS current_properties (
                                                id integer PRIMARY KEY,
                                                property_name text NOT NULL
                                              ); '''
    sql_create_property_durations_table = ''' CREATE TABLE IF NOT EXISTS property_durations (
                                                id integer PRIMARY KEY,
                                                created_at text NOT NULL,
                                                removed_at text NOT NULL
                                              ); '''
    sql_table_statements = [sql_create_properties_table,
                            sql_create_current_properties_table,
                            sql_create_property_durations_table]

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        for sql_table_statement in sql_table_statements:
            create_table(conn, sql_table_statement)
    else:
        print('Error! Cannot create the database connection.')

    conn.close()


if __name__ == '__main__':
    main()
