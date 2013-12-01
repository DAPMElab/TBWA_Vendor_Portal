
import template
import json

from sys import path
path.append('../')


class TestDataBlueprint(template.TestingTemplate):
    """ tests the methods in the data blueprint """

    def test_return_all_query_fail(self):
        """ test for failure with the /<dataset> API call """
        resp = self.request_with_role('/made_up_dataset',
            method='GET')
        self.check_error(resp, 'DATASET_NOT_FOUND')


    def test_return_all_query_success(self):
        """ test for success with the /<dataset> API call """
        resp = self.request_with_role('/test_dataset',
            method='GET')

        self.assertEqual(resp.status_code, 201)
        resp_data = json.loads(resp.data)['data']
        self.assertEqual(len(resp_data), len(template.expected_dataset))
        for line in resp_data:
            for col in ['id', 'col1', 'col2']:
                self.assertTrue(col in line)


    def test_return_all_dataset_names(self):
        """ tests that the endpoint returns all loaded datasets """
        resp = self.request_with_role('/datasets',
            method='GET')
         
        self.assertEqual(resp.status_code, 201)
        resp_data = json.loads(resp.data)['data']
        self.assertEqual(len(resp_data),
            len(template.test_dataset.keys()+template.test_tables))
        self.assertSetEqual(set(resp_data),
            set(template.test_dataset.keys()+template.test_tables))



