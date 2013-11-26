
import template
import json


class testReview(template.TestingTemplate):
    """ Tests the API endpoints associated with handling reviews. """

    def test_create_success(self):
        review = {'company': 'test', 'rating':10}
        resp = self.app.post('/review/create/123', data=json.dumps(review))
        self.assertEqual(resp.status_code, 200)

        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data['message'], 'review created')


    def test_create_fail(self):
        pass

    
    def test_approve_success(self):
        pass

    
    def test_approve_fail(self):
        pass


    def test_get_success(self):
        pass


    def test_get_fail(self):
        pass


    def test_edit_success(self):
        pass


    def test_edit_fail(self):
        pass


    def test_delete_success(self):
        pass


    def test_delete_fail(self):
        pass


    def test_list_success(self):
        pass


    def test_list_fail(self):
        pass

