
import template
import json

from sys import path
path.append('../')


class TestDataBlueprint(template.TestingTemplate):
    """ tests the methods in the data blueprint """


    def test_return_all_query_success(self):
        """ test for success with the /<dataset> API call """
        resp = self.request_with_role('/data',
            method='GET')

        self.assertEqual(resp.status_code, 201)
        resp_data = json.loads(resp.data)['data']
        self.assertEqual(len(resp_data), len(template.expected_dataset))
        for line in resp_data:
            for col in ['id', 'col1', 'col2']:
                self.assertTrue(col in line)



