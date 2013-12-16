
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


    def test_duplicate_email_failure(self):
        """ Test that /create fails with an existing email """
        admin = {
            'email'             :'duplicate_user@email.com',
            'password'          :'abc',
            'repeat_password'   :'abc'}
        resp = self.request_with_role('/admin/create', method='POST',
                data=json.dumps({'data': admin}))
        print resp.data
        self.assertEqual(201, resp.status_code)

        resp = self.request_with_role('/admin/create', method='POST',
                data=json.dumps({'data': admin}))
        self.check_error(resp, 'EMAIL_IN_USE')


    def test_create_success(self):
        """ Test sucess of /create with proper data """
        admin = {
            'email'             :'user_success@email.com',
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


    def _test_create_bad_email(self):
        # TODO: remove underscore when email verification is implemented
        " Test that /create fails with a bad email "
        admin = {'data':{'email': '123','password':'abc','repeat_password':'123'}}
        resp = self.request_with_role('/admin/create',
            method='POST',
            data=json.dumps(admin))
        self.check_error(resp, 'IMPROPER_EMAIL')


    def test_login_fail(self):
        """ Test that login fails w/ nonexistent users """

        # fails missing all data
        resp = self.request_with_role('/admin/login', method='POST')
        #self.check_error(resp, 'DATA_NEEDED_FOR_REQUEST')
        self.assertTrue('Please enter an email and password' in resp.data)

        # fails missing a password
        resp = self.request_with_role('/admin/login', method='POST',
                data={'email': 'missing pw'})
                #data=json.dumps({'data':{'email': 'missing pw'}}))
        #self.check_error(resp, 'MISSING_LOGIN_DATA')
        self.assertTrue('Please enter an email and password' in resp.data)
        
        # non_existent admin
        resp = self.request_with_role('/admin/login', method='POST',
                data=dict(email='non_existent@admin.com',password='insecure'))
                #data=json.dumps({'data':{
                #        'email': 'non_existent@admin.com',
                #        'password': 'insecure'}}))
        #self.check_error(resp, 'ADMIN_DNE')
        self.assertTrue('Admin does not exist' in resp.data)

        # incorrect password, make user then check
        admin = {
            'email'             :'login_user@email.com',
            'password'          :'abc',
            'repeat_password'   :'abc'}
        resp = self.request_with_role('/admin/create', method='POST',
                data=json.dumps({'data': admin}))
        print resp.data
        self.assertEqual(201, resp.status_code)

        
        admin['password'] = 'wrong'
        del admin['repeat_password']
        resp = self.request_with_role('/admin/login', method='POST',data=admin)
                #data=json.dumps({'data':admin}))
        #self.check_error(resp, 'INCORRECT_PASSWORD')
        self.assertTrue('Incorrect password' in resp.data)


    def test_login_success(self):
        """ Test that the login works with valid info """
        admin = {
            'email'             :'login_success_user@email.com',
            'password'          :'abc',
            'repeat_password'   :'abc'}

        # making user
        resp = self.request_with_role('/admin/create', method='POST',
                data=json.dumps({'data': admin}))
        self.assertEqual(201, resp.status_code)
        del admin['repeat_password']

        # login attempt
        with template.app.test_client() as c:
            resp = c.open(  # make request
                    path='/admin/login',
                    method='POST',
                    data=admin)
                    #data=json.dumps({'data':admin}))
            #self.assertEqual(201, resp.status_code)
            self.assertTrue('<title>Redirecting...</title>'
                    in resp.data)

            with c.session_transaction() as sess:
                # confirm the session was changed
                self.assertEqual(sess['role'], 'admin')
                self.assertEqual(sess['email'], admin['email'])


if __name__ == '__main__':
    unittest.main()


