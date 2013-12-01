
import template
import json
import rethinkdb as r
import unittest

TABLE = 'admin'

class TestAdmin(template.TestingTemplate):

    def test_create_bad_data(self):
        " Test that /create fails with improper datatypes and missing data "
        admin = {'data':{'email': '123','password':'abc','repeat_password':123}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))

        self.check_error(resp, 'ADMIN_DATA_NEEDED')

        # missing data
        admin = {'data':{'email': 123}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))

        self.check_error(resp, 'ADMIN_DATA_NEEDED')
        admin = {'data':{'email': 123,'password':'123'}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'ADMIN_DATA_NEEDED')

        # wrong datatypes
        admin = {'data':{'email': 123,'password':'123','repeat_password':'123'}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'ADMIN_DATA_NEEDED')

        admin = {'data':{'email':'123','password':'abc','repeat_password':'123'}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'ADMIN_DATA_NEEDED')

        admin = {'data':{'email': '123','password':'abc','repeat_password':123}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'ADMIN_DATA_NEEDED')


    # TODO: remove underscore when implemented
    def _test_create_bad_email(self):
        " Test that /create fails with a bad email "
        admin = {'data':{'email': '123','password':'abc','repeat_password':'123'}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'IMPROPER_EMAIL')


if __name__ == '__main__':
    unittest.main()


