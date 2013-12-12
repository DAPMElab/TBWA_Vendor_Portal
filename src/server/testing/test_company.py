
import template
import json
import unittest
import rethinkdb as r

TABLE = 'companies'


class TestCompany(template.TestingTemplate):
    """ Tests the API endpoints associated with handling companies. """

    def __create_company(self, company=
            {'name': 'test company', 'website': 'http://www.fake.com'}):
        """ method for use in the tests """
        resp = self.request_with_role('/company/create',
            method='POST', role='admin',
            data=json.dumps(company))
        self.assertEqual(resp.status_code, 201)
        return json.loads(resp.data)['uid']


    def test_create_company(self):
        """ Tests a successful company creation """
        company = {'name': 'test company', 'website': 'http://www.fake.com'}
        resp = self.request_with_role('/company/create',
            method='POST', role='admin',
            data=json.dumps(company))

        # testing creation
        print resp.data
        self.assertEqual(resp.status_code, 201)


    def test_create_fail(self):
        """ Make a request w/o data """
        resp = self.request_with_role('/company/create',
            method='POST', role='admin')
        self.check_error(resp, 'DATA_NEEDED_FOR_REQUEST')

        company = {'name': 'missing website'}
        resp = self.request_with_role('/company/create',
            method='POST', role='admin', data=json.dumps(company))
        self.check_error(resp, 'DATA_NEEDED_FOR_REQUEST')


    def test_get_success(self):
        """ tests successfully returning a company via get """
        uid = self.__create_company()

        # getting company
        resp = self.request_with_role('/company/get/{}'.format(uid))

        # testing response
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data['message'], 'company found')


    def test_get_fail(self):
        """ tests failing to return via /get """
        # getting non existent company
        resp = self.request_with_role('/company/get/{}'.format('fake_company'))

        # testing response
        self.check_error(resp, 'COMPANY_NOT_FOUND')




