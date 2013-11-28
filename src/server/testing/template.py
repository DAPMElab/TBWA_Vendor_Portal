
import unittest
import rethinkdb
#import template
import json

from sys import path
path.append('../')
from data import setup_db
from app import app
from config.errors import errors


import os
this_dir = os.path.dirname(__file__)
test_csv = os.path.join(this_dir, 'data_test.csv')
test_dataset = {'test_dataset': test_csv}
test_tables = ['test_table', 'reviews']

expected_dataset = [
        {'col1':'this','col2':'should'},
        {'col1':'work','col2':'hopefully'}]


class TestingTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Sets up a test database before each set of tests """
        setup_db('localhost', 28015, 'TEST',
            datasets = test_dataset,
            app_tables = test_tables)
        self.rdb = rethinkdb.connect(
                host = 'localhost',
                port = 28015,
                db = 'TEST')
        self.rdb.use('TEST')
        app.config['RDB_DB'] = 'TEST'
        self.app = app.test_client()


    @classmethod
    def tearDownClass(self):
        """ Drops the test database after the classes' tests are finished """
        with rethinkdb.connect(host='localhost', port=28015) as conn:
            if 'TEST' in rethinkdb.db_list().run(conn):
                rethinkdb.db_drop('TEST').run(conn)
        try:
            self.rdb.close()
        except AttributeError:
            pass
           

    def check_error(self, resp, error_name):
        """ Tests that the resp is equal to the specified error """
        expected_error = errors['english'][error_name]

        self.assertEqual(resp.status_code, expected_error['status_code'])
        self.assertEqual(
            json.loads(resp.data),
            {
                u'message':     expected_error['message'],
                u'status_code': expected_error['status_code']
            }
        )

