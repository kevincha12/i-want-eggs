import psycopg2
import os
from dotenv import load_dotenv
from exception import TransactionNotOpenError

class DBHandler:
    
    #btw, the db has to already exist. like, this code provides the schema for the table setup,
    #but it won't make the actual db instance for you. the DB_NAME provided MUST exist.
    def __init__(self):
        load_dotenv()
        self.db_name = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.pw = os.getenv('DB_PW')

    def open_conn(self):
        self.conn = psycopg2.connect(f'dbname={self.db_name} user={self.user} password={self.pw}')
    
    def close_conn(self):
        self.conn.close()

    def new_transaction(self):
        self.curs = self.conn.cursor()

    def close_transaction(self):
        self.curs.close()

    def rollback(self):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.conn.rollback()

    def commit(self):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.conn.commit()

    def create_tables(self):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        CREATE TABLE IF NOT EXISTS stores (
                          id SERIAL PRIMARY KEY,
                          address VARCHAR UNIQUE,
                          city VARCHAR,
                          zipcode VARCHAR,
                          longitude NUMERIC NOT NULL,
                          latitude NUMERIC NOT NULL
                          )
                          ''')
        self.curs.execute('''
                        CREATE TABLE IF NOT EXISTS eggs (
                          id SERIAL PRIMARY KEY,
                          name VARCHAR NOT NULL,
                          price NUMERIC NOT NULL
                          )
                          ''')
        self.curs.execute('''
                        CREATE TABLE IF NOT EXISTS store_egg_relation (
                          id SERIAL PRIMARY KEY,
                          store INTEGER NOT NULL,
                          egg INTEGER NOT NULL,
                          FOREIGN KEY (store) REFERENCES stores (id) ON DELETE CASCADE,
                          FOREIGN KEY (egg) REFERENCES eggs (id) ON DELETE CASCADE
                          )
                          ''')

    def drop_tables(self):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        DROP TABLE IF EXISTS stores, eggs, store_egg_relation
                          ''')
    
    def add_store(self, address, city, zipcode, longitude, latitude):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        INSERT INTO stores (address, city, zipcode, longitude, latitude)
                          VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                          ''',
                        (address, city, zipcode, longitude, latitude)
                          )
        store_pkey = self.curs.fetchone()[0]
        return store_pkey
        
        
    def add_egg(self, name, price):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        INSERT INTO eggs (name, price)
                          VALUES (%s, %s)
                        RETURNING id
                          ''',
                        (name, price)
                          )
        egg_pkey = self.curs.fetchone()[0]
        return egg_pkey
    
    def add_store_egg_relation(self, store_pkey, egg_pkey):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        INSERT INTO store_egg_relation (store, egg)
                          VALUES(%s, %s)
                          ''',
                          (store_pkey, egg_pkey)
                          )
    
    def get_store_by_address(self, store_address):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        SELECT * FROM stores
                          WHERE address = %s
                          ''',
                        (store_address,)
                          )
        store = self.curs.fetchone()
        return store

    def get_eggs_for_store(self, store_pkey):
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        SELECT eggs.* FROM eggs
                          INNER JOIN store_egg_relation ON eggs.id = store_egg_relation.egg
                          WHERE store = %s
                          ''',
                        (store_pkey,)
                          )
        eggs = self.curs.fetchall()
        return eggs

    def get_all_stores(self):
        #note that this does NOT get you enough for a store object, you MUST also
        #get the eggs for a given store :)
        if self.curs.closed:
            raise TransactionNotOpenError
        self.curs.execute('''
                        SELECT * FROM stores
                          ''')
        stores = self.curs.fetchall()
        return stores