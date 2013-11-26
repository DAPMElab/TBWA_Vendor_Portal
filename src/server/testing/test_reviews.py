
import template
import json


class testReview(template.TestingTemplate):
    """ Tests the API endpoints associated with handling reviews. """

    def test_create_success(self):
        """ Tests a successful review creation """
        # creating review
        review = {'company': 'test', 'rating':10}
        resp = self.app.post('/review/create/123', data=json.dumps(review))

        # testing creation
        self.assertEqual(resp.status_code, 201)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data['message'], 'review created')


    def test_create_fail(self):
        # don't know how to get this to fail yet
        pass

    
    def test_approve_success(self):
        """ Tests successfully updating a review to approved """
        # creating review
        review = {'company': 'test', 'rating':10}
        resp = self.app.post('/review/create/123', data=json.dumps(review))
        rid = json.loads(resp.data)['uid']

        # approving review
        resp = self.app.post('/review/approve/{}'.format(rid))

        # testing approval
        self.assertEqual(resp.status_code, 200)
        approve_resp_data = json.loads(resp.data)
        self.assertEqual(approve_resp_data['message'], 'review approved')
        resp = self.app.get('/review/get/{}'.format(rid))
        get_resp_data = json.loads(resp.data)
        self.assertTrue(get_resp_data['data']['approved'])
    

    def test_approve_fail(self):
        """ Tests successfully updating a review to approved """
        # approving review
        resp = self.app.post('/review/approve/{}'.format('WRONG'))

        # testing approval
        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.data)
        self.check_error(resp, 'REVIEW_APPROVAL_FAILURE')


    def test_get_success(self):
        """ Tests returning a review """
        # creating review
        review = {'company': 'test', 'rating':10, 'submitter': 'tester'}
        resp = self.app.post('/review/create/123', data=json.dumps(review))
        rid = json.loads(resp.data)['uid']

        # getting review
        resp = self.app.get('/review/get/{}'.format(rid))

        # testing response
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.data)
        review['approved'] = False      # update obj
        self.assertDictEqual(resp_data['data'], review)


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

