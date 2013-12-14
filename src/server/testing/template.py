
import unittest
import rethinkdb
import json

from sys import path
path.append('../')
from data           import setup_db
from app            import app
from config.errors  import errors


import os
this_dir = os.path.dirname(__file__)
test_json = os.path.join(this_dir, 'data_test.json')

test_dataset = {'companies': test_json}
test_tables = ['test_table', 'reviews', 'admin']


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


    def request_with_role(self, path, method='GET', role='admin', *args, **kwargs):
        """ Make an http request with the given role in the session """
        #with self.app_ref.test_client() as c:
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['role'] = role
                kwargs['method'] = method
                kwargs['path'] = path
            return c.open(*args, **kwargs)


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

