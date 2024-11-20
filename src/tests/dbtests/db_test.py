import unittest
import sqlalchemy
#from sqlalchemy import text
import testing.postgresql
import psycopg2
import database
#import app


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()
        self.db_conf = self.postgresql.dsn()
        #self.session = 
        # Create a connection which can be used by our test functions to set and
        # query the state of the database
        self.conn = psycopg2.connect(**self.db_conf)
        #self.conn = self.postgresql
        #self.cursor = self.conn.cursor()
        #engine = sqlalchemy.create_engine(self.pgsql.url())
        # Create an 'employees' table and insert test records.
        #self.cursor.execute(sql)
        #self.cursor.execute("INSERT INTO Articles (author, title, journal, year) VALUES ('m', 'm', 'm', 1)")
        #self.conn.commit()
        sql = """CREATE TABLE IF NOT EXISTS Articles (id SERIAL PRIMARY KEY,
            author  TEXT NOT NULL,
            title   TEXT NOT NULL,
            journal TEXT NOT NULL,
            year    INT  NOT NULL,
            volume  INT,
            number  INT,
            pages   INT,
            month   INT,
            note    TEXT,

            UNIQUE (author, title)
        );"""
        self.session.execite
    
    def tearDown(self):
        # Close the database cursor and the database connection.
        #self.cursor.close()
        self.conn.close()
        self.postgresql.stop()
    
    def test_database_query(self):
        with self.conn.cursor() as self.cur:
            self.add_article('m', 'm', 'm', 1)
        results = database.get_all_articles()
        expected_results = [('m', 'm', 'm', 1)]
        self.assertEqual(results, expected_results)
    
    def test_database_duplicate(self):
        database.add_article('m', 'm', 'm', 1)
        results = database.add_article('m', 'm', 'm', 1)
        # Assert that the results match the expected results.
        self.assertEqual(results, False)









#def slurp(path):
        #with open(path, 'r') as f:
            #return f.read()


#def setUp(self):
    #self.postgresql = testing.postgresql.Postgresql()
    #self.db_conf = self.postgresql.dsn()
    # Create a connection which can be used by our test functions to set and
    # query the state of the database
    #self.conn = psycopg2.connect(**self.db_conf)
    #self.conn = self.postgresql
    #self.cursor = self.conn.cursor()
    #engine = sqlalchemy.create_engine(self.pgsql.url())
    # Create an 'employees' table and insert test records.
    #self.cursor.execute(sql)
    #self.cursor.execute("INSERT INTO Articles (author, title, journal, year) VALUES ('m', 'm', 'm', 1)")
    #self.conn.commit()
    #self.sql = """CREATE TABLE IF NOT EXISTS Articles (id SERIAL PRIMARY KEY,
                #author  TEXT NOT NULL,
                #title   TEXT NOT NULL,
                #journal TEXT NOT NULL,
                #year    INT  NOT NULL,
                #volume  INT,
                #number  INT,
                #pages   INT,
                #month   INT,
                #note    TEXT,

                #UNIQUE (author, title)
                #);"""
    #with self.conn.cursor() as self.cur:
        # Create the initial database structure (roles, schemas, tables etc.)
        # basically anything that doesn't change './setup.sql'
        #db = open('./setup.sql').read()
        #self.cur.execute(slurp(self.sql))
    
#def tearDown(self):
    # Close the database cursor and the database connection.
    #self.cursor.close()
    #self.conn.close()
    #self.postgresql.stop()

#def test_database_query(self):
    #results = database.add_article('m', 'm', 'm', 1)
    # Define the expected results as a list of tuples.
    #expected_results = [('m', 'm')]

    # Assert that the results match the expected results.
    #self.assertEqual(results, expected_results)

#def test_database_duplicate(self):
    # Define the expected results as a list of tuples.
    #expected_results = [('m', 'm')]
    #database.add_article('m', 'm', 'm', 1)
    #results = database.add_article('m', 'm', 'm', 1)
    # Assert that the results match the expected results.
    #self.assertEqual(results, False)


#class TestDatabase(unittest.TestCase):
    #def setUp(self):
        #self.postgresql = testing.postgresql.Postgresql()
        #self.db_conf = self.postgresql.dsn()
        #self.session = 
        # Create a connection which can be used by our test functions to set and
        # query the state of the database
        #self.conn = psycopg2.connect(**self.db_conf)
        #self.conn = self.postgresql
        #self.cursor = self.conn.cursor()
        #engine = sqlalchemy.create_engine(self.pgsql.url())
        # Create an 'employees' table and insert test records.
        #self.cursor.execute(sql)
        #self.cursor.execute("INSERT INTO Articles (author, title, journal, year) VALUES ('m', 'm', 'm', 1)")
        #self.conn.commit()
        #self.sql = """CREATE TABLE IF NOT EXISTS Articles (id SERIAL PRIMARY KEY,
                    #author  TEXT NOT NULL,
                    #title   TEXT NOT NULL,
                    #journal TEXT NOT NULL,
                    #year    INT  NOT NULL,
                    #volume  INT,
                    #number  INT,
                    #pages   INT,
                    #month   INT,
                    #note    TEXT,

                    #UNIQUE (author, title)
                    #);"""
        #with self.conn.cursor() as self.cur:
            # Create the initial database structure (roles, schemas, tables etc.)
            # basically anything that doesn't change './setup.sql'
            #db = open('./setup.sql').read()
            #self.cur.execute(slurp(self.sql))
        #self.session = (self.sql)
    
    #def tearDown(self):
        # Close the database cursor and the database connection.
        #self.cursor.close()
        #self.conn.close()
        #self.postgresql.stop()
    
    #def test_database_query(self):
        #with self.conn.cursor() as self.cur:
            #self.cur.execute(slurp("SELECT author, title FROM Articles"))
            #results = self.cur.fetchall()
        #results = database.add_article('m', 'm', 'm', 1)
        # Define the expected results as a list of tuples.
        #expected_results = [('m', 'm')]

        # Assert that the results match the expected results.
        #self.assertEqual(results, expected_results)
    
    #def test_database_duplicate(self):
        #with self.conn.cursor() as self.cur:
            #self.cur.execute(slurp("INSERT INTO Articles (author, title, journal, year) VALUES ('m', 'm', 'm', 1)"))
            #self.cur.execute(slurp("SELECT author, title FROM Articles"))
            #results = self.cur.fetchall()
        # Define the expected results as a list of tuples.
        #expected_results = [('m', 'm')]
        #database.add_article('m', 'm', 'm', 1)
        #results = database.add_article('m', 'm', 'm', 1)
        # Assert that the results match the expected results.
        #self.assertEqual(results, False)

#if __name__ == '__main__':
    #unittest.main()
