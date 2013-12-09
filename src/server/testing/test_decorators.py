
import unittest
import template

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


if __name__ == '__main__':
    unittest.main()

