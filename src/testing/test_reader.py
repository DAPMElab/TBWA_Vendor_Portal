
from copy import deepcopy
import rethinkdb

from sys import path
path.append('../')
from data import reader

import os
this_dir = os.path.dirname(__file__)
test_csv = os.path.join(this_dir, 'data_test.csv')

expected_dataset = [
        {'col1':'this','col2':'should'},
        {'col1':'work','col2':'hopefully'}]


from template import TestingTemplate

class TestCSVReader(TestingTemplate):
    """ Tests that the reader module functions correctly """

    @classmethod
    def setUpClass(self):
        """ Overriding this so the database is not setup """
        pass


    def test_get_data_bad_dataset_name(self):
        """ Tests that the reader fails when given an invalid dataset name """
        with self.assertRaises(Exception):
            reader.get_data('non-existent dataset')


    def test_get_data(self):
        """ Tests that a reader object is returned """
        data = reader.get_data('test', path_to_data=test_csv)
        self.assertEqual(data, expected_dataset)


    def test_setup_db(self):
        """ Test creation of a db and tables """
        dataset = {'test': test_csv}
        reader.setup_db('localhost', 28015, 'TEST', datasets=dataset)

        with rethinkdb.connect(host='localhost', port=28015) as conn:

            # test that the 'TEST' database was created
            db_list = rethinkdb.db_list().run(conn)
            self.assertTrue('TEST' in db_list)
            conn.use('TEST')

            # test that the 'test' table was created
            table_list = rethinkdb.table_list().run(conn)
            self.assertEqual(1, len(table_list))
            self.assertEqual('test', table_list[0])

            # test that the data is correct by checking columns
            data = [row for row in rethinkdb.table('test').run(conn)]
            self.assertSetEqual(
                set(data[0].keys())-set([u'id']),
                set(expected_dataset[0].keys()))

if __name__ == '__main__':
    unittest.main()

