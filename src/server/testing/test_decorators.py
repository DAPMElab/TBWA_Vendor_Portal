
# TODO: Figure out a better way of testing this. Possible a test app that uses
#       the decorators?

import rethinkdb as r
import unittest
import template
import json

from sys import path
path.append('../')
from blueprints import decorators


class TestDecorators(template.TestingTemplate):

    def test_admin_success(self):
        """ test that the call is allowed when the user is an admin """
        resp = self.request_with_role('/',
            role='admin')
        self.assertEqual(resp.status_code, 200)

        resp = self.request_with_role('/',
            role='user')
        self.assertEqual(resp.status_code, 200)

        resp = self.request_with_role('/review/list',
            role='admin')
        self.assertEqual(resp.status_code, 200)


    def test_admin_fail(self):
        """ test that the call is blocked when the user not an admin """
        resp = self.request_with_role('/review/list',
            role='user')
        self.check_error(resp, 'ADMIN_REQUIRED')


    def test_has_data_fail(self):
        """ test that the call passes w/ data """
        # makes the call w/o data
        resp = self.request_with_role('/review/create/123',
            method='POST')
        self.check_error(resp, 'DATA_NEEDED_FOR_REQUEST')


    def test_has_data_success(self):
        """ test that the call passes w/ data """
        # create fake company to link to
        outcome = r.table('companies').insert({
                'Name'  : 'Fake Company',
                'URL'   : 'Broken URL',
                'id'    : '123',
                'ReviewIds' : []
        }).run(self.rdb)

        # makes the call w/ data
        review = {'Submitter': 'test', 'Rating':10}
        resp = self.request_with_role('/review/create/123',
            method='POST', data=json.dumps(review))
        self.assertEqual(201, resp.status_code)


if __name__ == '__main__':
    unittest.main()


