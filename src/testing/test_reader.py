
from sys import path
path.append('../')
from data import reader

import os
this_dir = os.path.dirname(__file__)
test_csv = os.path.join(this_dir, 'test.csv')


import unittest

class TestCSVReader(unittest.TestCase):
    """ Tests that the reader module functions correctly """

    def test_bad_dataset_name(self):
        """ Tests that the reader fails when given an invalid dataset name """
        with self.assertRaises(Exception):
            reader.get_data('non-existent dataset')


    def test_read(self):
        """ Tests that a reader object is returned """
        col, data = reader.get_data('test', path_to_data=test_csv)

        expected_data = [['this','should'],['work','hopefully']]
        expected_columns = ['col1','col2']

        self.assertEqual(col, expected_columns)
        for row in data:
            self.assertEqual(row, expected_data.pop(0))


if __name__ == '__main__':
    unittest.main()

