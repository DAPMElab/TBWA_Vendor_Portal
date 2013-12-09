
import template
import json
import rethinkdb as r
import unittest
from passlib.hash import sha256_crypt

TABLE = 'admin'

class TestAdmin(template.TestingTemplate):

    def test_create_bad_data(self):
        """ Test that /create fails with missing data """

        # fail with missing passwords
        admin = {'data':{'email': 123}}
        resp = self.request_with_role('/admin/create', method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'ADMIN_DATA_NEEDED')

        # fail with missing repeat password
        admin = {'data':{'email': 123,'password':'123'}}
        resp = self.request_with_role('/admin/create', method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'ADMIN_DATA_NEEDED')

        # fail with mismatched passwords
        admin = {'data':{'email':'123','password':'abc','repeat_password':'123'}}
        resp = self.request_with_role('/admin/create', method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'PASSWORDS_UNMATCHED')

    
    def test_create_success(self):
        """ Test sucess of /create with proper data """

        admin = {
            'email'             :'user@email.com',
            'password'          :'abc',
            'repeat_password'   :'abc'}
        resp = self.request_with_role('/admin/create', method='POST',
                data=json.dumps({'data': admin}))

        self.assertEqual(201, resp.status_code)
        uid = json.loads(resp.data)['uid']

        db_admin = r.table('admin').get(uid).run(self.rdb)
        self.assertEqual(admin['email'], db_admin['email'])
        self.assertTrue(sha256_crypt.verify(
                admin['password'], db_admin['password']))
        self.assertFalse(sha256_crypt.verify(
                'break', db_admin['password']))



    def _test_create_bad_email(self):
        # TODO: remove underscore when email verification is implemented
        " Test that /create fails with a bad email "
        admin = {'data':{'email': '123','password':'abc','repeat_password':'123'}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'IMPROPER_EMAIL')


if __name__ == '__main__':
    unittest.main()


