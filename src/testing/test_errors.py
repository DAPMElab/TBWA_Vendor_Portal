
import unittest
import json

from sys import path
path.append('../')
from config.errors import errors as declared_errors
from config.errors import construct_err


class TestErrorGenerator(unittest.TestCase):

    def test_generator_default(self):
        """ test that the generator correctly creates an error """
        err_data, err_code = construct_err()
        err_data = json.loads(err_data)

        self.assertDictEqual(declared_errors['english']['DEFAULT'], err_data)


    def test_generator_name_fail(self):
        """ test that the generator correctly defaults with a bad err name """
        err_data, err_code = construct_err(err_name='imaginary error')
        err_data = json.loads(err_data)

        self.assertDictEqual(declared_errors['english']['DEFAULT'], err_data)


    def test_generator_language_fail(self):
        """ test that the generator correctly defaults with a bad language """
        err_data, err_code = construct_err(err_language='klingon')
        err_data = json.loads(err_data)

        self.assertDictEqual(declared_errors['english']['DEFAULT'], err_data)


    def test_generator_success(self):
        """ test that the generator correctly creates an error """
        err_data, err_code = construct_err(err_name='NO_DB_CONN')
        err_data = json.loads(err_data)

        self.assertDictEqual(declared_errors['english']['NO_DB_CONN'], err_data)

