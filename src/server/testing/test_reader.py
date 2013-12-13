
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


    def test_setup_db(self):
        """ Test creation of a db and tables """
        # test that the 'TEST' database doesn't exist
        with rethinkdb.connect(host='localhost', port=28015) as conn:
            db_list = rethinkdb.db_list().run(conn)
            self.assertTrue('TEST' not in db_list)

        creations = self.run_setup_db()

        # confirm the correct tables were created
        self.assertSetEqual(creations,
            set(template.test_dataset.keys()+template.test_tables))

        with rethinkdb.connect(host='localhost', port=28015) as conn:
            # test that the 'TEST' database was created
            db_list = rethinkdb.db_list().run(conn)
            self.assertTrue('TEST' in db_list)
            conn.use('TEST')

            # test that the 'test' table was created
            table_list = rethinkdb.table_list().run(conn)
            self.assertEqual(len(table_list),
                len(template.test_dataset.keys()+template.test_tables))
            self.assertTrue(template.test_dataset.keys()[0] in table_list)

            # test that the data is correct by checking columns
            data = [row for row in rethinkdb.table(
                template.test_dataset.keys()[0]).run(conn)]
            self.assertSetEqual(
                set(data[0].keys())-set([u'id']),
                set(template.expected_dataset[0].keys()))

        self.run_clear_test_db()


    def test_setup_db_insert_choices(self):
        creations = self.run_setup_db()
        print creations

        # confirm the correct tables were created
        self.assertSetEqual(creations,
            set(template.test_dataset.keys() + template.test_tables))


    def run_setup_db(self):
        return reader.setup_db(
            'localhost',    # host
            28015,          # port
            'TEST',         # db name
            datasets    = template.test_dataset,    # datasets
            app_tables  = template.test_tables)     # tables


    def run_clear_test_db(self):
        """ Drops the test database """
        with rethinkdb.connect(host='localhost', port=28015) as conn:
            if 'TEST' in rethinkdb.db_list().run(conn):
                rethinkdb.db_drop('TEST').run(conn)


if __name__ == '__main__':
    unittest.main()

