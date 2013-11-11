
import rethinkdb
import template

from sys import path
path.append('../')
from data import reader


class TestCSVReader(template.TestingTemplate):
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
        data = reader.get_data('test', path_to_data=template.test_csv)
        self.assertEqual(data, template.expected_dataset)


    def test_setup_db(self):
        """ Test creation of a db and tables """
        reader.setup_db('localhost', 28015, 'TEST',
            datasets=template.test_dataset)

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
                set(template.expected_dataset[0].keys()))

if __name__ == '__main__':
    unittest.main()

