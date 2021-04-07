import os
import sqlite3
from sqlite3 import Error


def make_db_dir(path_to_dir):
    """ create new directory to store sqlite3 database file
    :param path_to_dir: absolute path for new database directory
    :return:
    """
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)


def create_connection(db_file):
    """ create database connection to SQLite database and create database if database does not already exist
    :param db_file: database file
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    make_db_dir(f'{os.getcwd()}{os.sep}db')
    create_connection(f'{os.getcwd()}{os.sep}db{os.sep}listings.db')

