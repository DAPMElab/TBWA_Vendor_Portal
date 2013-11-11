
import unittest
from data import reader
import rethinkdb

from sys import path
path.append('../')
from data import reader

class TestingTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Sets up a test database before each set of tests """
        reader.setup_db('localhost', 28015, 'TEST')
        self.rdb = rethinkdb.connect(
                host = 'localhost',
                port = 28015,
                db = 'TEST')



    @classmethod
    def tearDownClass(self):
        """ Drops the test database after  """
        with rethinkdb.connect(host='localhost', port=28015) as conn:
            rethinkdb.db_drop('TEST').run(conn)
        try:
            self.rdb.close()
        except AttributeError:
            pass
            

