
import template
import json
import unittest

from sys import path
path.append('../')


class TestDataBlueprint(template.TestingTemplate):
    """ tests the methods in the data blueprint """

    def test_return_all_query_fail(self):
        """ test for failure with the /<dataset> API call """
        resp = self.app.get('/made_up_dataset')
        self.check_error(resp, 'DATASET_NOT_FOUND')


    def test_return_all_query_success(self):
        """ test for success with the /<dataset> API call """
        resp = self.app.get('/test')
        self.assertEqual(resp.status_code, 201)

