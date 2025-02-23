import psycopg2
import os
from dotenv import load_dotenv
from exception import ConnectionNotOpenError

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

    def rollback(self):
        if self.conn.closed:
            raise ConnectionNotOpenError
        self.conn.rollback()

    def commit(self):
        if self.conn.closed:
            raise ConnectionNotOpenError
        self.conn.commit()

    def create_tables(self):
        if self.conn.closed:
            raise ConnectionNotOpenError
        self.conn.execute('''
                        CREATE TABLE IF NOT EXISTS stores (
                          id SERIAL PRIMARY KEY,
                          address VARCHAR UNIQUE,
                          city VARCHAR,
                          zipcode VARCHAR,
                          longitude NUMERIC NOT NULL,
                          latitude NUMERIC NOT NULL
                          )
                          ''')
        self.conn.execute('''
                        CREATE TABLE IF NOT EXISTS eggs (
                          id SERIAL PRIMARY KEY,
                          name VARCHAR NOT NULL,
                          price INTEGER NOT NULL
                          )
                          ''')
        self.conn.execute('''
                        CREATE TABLE IF NOT EXISTS store_egg_relation (
                          id SERIAL PRIMARY KEY,
                          store INTEGER NOT NULL,
                          egg INTEGER NOT NULL,
                          FOREIGN KEY (store) REFERENCES stores (id) ON DELETE CASCADE,
                          FOREIGN KEY (egg) REFERENCES eggs (id) on ON DELETE CASCADE
                          )
                          ''')

    def drop_tables(self):
        if self.conn.closed:
            raise ConnectionNotOpenError
        self.conn.execute('''
                        DROP TABLE IF EXISTS stores, eggs, store_egg_relaton
                          ''')
    
    def add_store(self, address, city, zipcode, longitude, latitude):
        if self.conn.closed:
            raise ConnectionNotOpenError
        curs = self.conn.execute('''
                        INSERT INTO stores (address, city, zipcode, longitude, latitude)
                          VALUES (%s, %s, %s, %f, %f)
                        RETURNING id
                          ''',
                        (address, city, zipcode, longitude, latitude)
                          )
        store_pkey = curs.fetchone()[0]
        curs.close()
        return store_pkey
        
        
    def add_egg(self, name, price):
        if self.conn.closed:
            raise ConnectionNotOpenError
        curs = self.conn.execute('''
                        INSERT INTO eggs (name, price)
                          VALUES (%s, %f)
                        RETURNING id
                          ''',
                        (name, price)
                          )
        egg_pkey = curs.fetchone()[0]
        curs.close()
        return egg_pkey
    
    def add_store_egg_relation(self, store_pkey, egg_pkey):
        if self.conn.closed:
            raise ConnectionNotOpenError
        self.conn.execute('''
                        INSERT INTO store_egg_relation (store, egg)
                          VALUES(%d, %d)
                          ''',
                          (store_pkey, egg_pkey)
                          )
    
    def get_store_by_address(self, store_address):
        if self.conn.closed:
            raise ConnectionNotOpenError
        curs = self.conn.execute('''
                        SELECT * FROM stores
                          WHERE address = %s
                          ''',
                        (store_address,)
                          )
        store = curs.fetchone()
        curs.close()
        return store

    def get_eggs_for_store(self, store_pkey):
        if self.conn.closed:
            raise ConnectionNotOpenError
        curs = self.conn.execute('''
                        SELECT eggs.* FROM eggs
                          INNER JOIN store_egg_relation ON eggs.id = store_egg_relation.egg
                          WHERE store = %s
                          ''',
                        (store_pkey,)
                          )
        eggs = curs.fetchall()
        curs.close()
        return eggs

    def get_all_stores(self):
        #note that this does NOT get you enough for a store object, you MUST also
        #get the eggs for a given store :)
        if self.conn.closed:
            raise ConnectionNotOpenError
        curs = self.conn.execute('''
                        SELECT * FROM stores
                          ''')
        stores = curs.fetchall()
        curs.close()
        return stores