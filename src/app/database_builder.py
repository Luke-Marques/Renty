import os
import sqlite3
from sqlite3 import Error


class DatabaseBuilder:

    def __init__(self, database_filename):
        self.database_filename = database_filename

    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_filename)
            return conn
        except Error as e:
            print(e)

        return conn

    def new_table(self, table):
        conn = self.connect()

        if table == 'properties':
            sql_table_statement = \
                f'''CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    num_bed INTEGER,
                    property_type TEXT,
                    rent_pcm INTEGER,
                    description TEXT,
                    agent TEXT,
                    agent_region TEXT,
                    address TEXT,
                    postcode TEXT
                );'''
        elif table == 'dates':
            sql_table_statement = \
                f'''CREATE TABLE IF NOT EXISTS {table} (
                    property_id integer PRIMARY KEY,
                    first_seen_at TEXT,
                    listed_at TEXT,
                    last_seen_at TEXT
                );'''

        try:
            c = conn.cursor()
            c.execute(sql_table_statement)
        except Error as e:
            print(e)

        conn.commit()
        print('Table created :', table)
        conn.close()

    def insert_data(self, table, data):
        conn = self.connect()

        if table == 'properties':
            cols = ['id', 'title', 'num_bed', 'property_type', 'rent_pcm',
                    'description', 'agent', 'agent_region', 'address', 'postcode']
        elif table == 'dates':
            cols = ['property_id', 'first_seen_at', 'listed_at', 'last_seen_at']

        values = ['?' for i in range(len(cols))]

        sql_insert_statement = f'''INSERT INTO {table}({', '.join(cols)}) VALUES({', '.join(values)})'''

        c = conn.cursor()


        c.execute(sql_insert_statement, data)

        conn.commit()
        last_row_id = c.lastrowid
        conn.close()

        return last_row_id
