
import template
import json
import unittest
import rethinkdb as r

TABLE = 'reviews'


class TestReview(template.TestingTemplate):
    """ Tests the API endpoints associated with handling reviews. """

    def __create_review(self, review={'company': 'test', 'rating':10}):
        """ method for use in the tests """
        resp = self.request_with_role('/review/create/123',
            method='POST',
            data=json.dumps(review))
        self.assertEqual(resp.status_code, 201)
        return json.loads(resp.data)['uid']


    def test_create_success(self):
        """ Tests a successful review creation """
        #TODO: make /create calls log their ID as the company id
        # creating review
        review = {'company': 'test', 'rating':10}
        resp = self.request_with_role('/review/create/123',
            method='POST',
            data=json.dumps(review))

        # testing creation
        self.assertEqual(resp.status_code, 201)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data['message'], 'review created')


    def test_create_fail(self):
        """ Make a request w/o data """
        resp = self.request_with_role('/review/create/123',
            method='POST')
        self.check_error(resp, 'DATA_NEEDED_FOR_REQUEST')

    
    def test_approve_success(self):
        """ Tests successfully updating a review to approved """
        # creating review
        review = {'company': 'test', 'rating':10}
        resp = self.request_with_role('/review/create/123',
            method='POST',
            data=json.dumps(review))
        rid = json.loads(resp.data)['uid']

        # approving review
        resp = self.request_with_role('/review/approve/{}'.format(rid),
            method='POST')

        # testing approval
        self.assertEqual(resp.status_code, 200)
        approve_resp_data = json.loads(resp.data)
        self.assertEqual(approve_resp_data['message'], 'review approved')
        resp = self.request_with_role('/review/get/{}'.format(rid),
            method='GET')
        get_resp_data = json.loads(resp.data)
        self.assertTrue(get_resp_data['data']['approved'])
    

    def test_approve_fail(self):
        """ Tests successfully updating a review to approved """
        # approving review
        resp = self.request_with_role('/review/approve/{}'.format('WRONG'),
            method='POST')

        # testing approval
        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.data)
        self.check_error(resp, 'REVIEW_APPROVAL_FAILURE')


    def test_get_success(self):
        """ Tests returning a review """
        review = {'company': 'test', 'rating':10}
        rid = self.__create_review()

        # getting review
        resp = self.request_with_role('/review/get/{}'.format(rid),
            method='GET')

        # testing response
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.data)
        review['approved'] = False      # update obj
        self.assertDictEqual(resp_data['data'], review)


    def test_get_fail(self):
        """ Tests returning a review that doesn't exist """
        # getting a non-existent review
        resp = self.request_with_role(
            '/review/get/{}'.format('nonexistent_reivew'),
            method='GET')
        self.check_error(resp, 'REVIEW_NOT_FOUND')


    def test_edit_success(self):
        """ Test that a review properly updates """
        # creating a review
        review = {'company': 'test', 'rating':10, 'submitter': 'tester'}
        resp = self.request_with_role('/review/create/123',
            method='POST',
            data=json.dumps(review))
        rid = json.loads(resp.data)['uid']

        # updating review
        review['rating'] = 5
        resp = self.request_with_role('/review/edit/{}'.format(rid),
            method='PATCH',
            data=json.dumps(review))
        self.assertEqual(resp.status_code, 200)

        # getting review
        resp_get = self.request_with_role('/review/get/{}'.format(rid),
            method='GET')
        self.assertEqual(resp_get.status_code, 200)
        data_get = json.loads(resp_get.data)
        self.assertEqual(data_get['data']['rating'], 5)


    def test_edit_fail(self):
        """ Test that /edit fails with a bad id """
        resp = self.request_with_role(
            '/review/edit/{}'.format('nonexistent_review'),
            method='PATCH')

        self.check_error(resp, 'DATA_NEEDED_FOR_REQUEST')

        resp = self.request_with_role(
            '/review/edit/{}'.format('nonexistent_review'),
            method='PATCH',
            data=json.dumps({'mock':'data'}))
        self.check_error(resp, 'REVIEW_NOT_FOUND')


    def test_delete_success(self):
        """ Test that a review is properly deleted """
        # creating a review
        review = {'company': 'test', 'rating':10, 'submitter': 'tester'}
        resp = self.request_with_role('/review/create/123',
            method='POST',
            data=json.dumps(review))
        rid = json.loads(resp.data)['uid']

        # deleting review
        delete_resp = self.request_with_role('/review/delete/{}'.format(rid),
            method='DELETE')

        self.assertEqual(delete_resp.status_code, 202)
        delete_data = json.loads(delete_resp.data)
        self.assertEqual(delete_data['message'],
            'review deleted')

        # trying to get the review
        resp = self.request_with_role('review/get/{}'.format(rid),
            method='GET')
        self.check_error(resp, 'REVIEW_NOT_FOUND')


    def test_delete_fail(self):
        """ Test that /delete properly fails when there's no id match """
        num_before = r.table(TABLE).count().run(self.rdb)

        # deleting review
        resp = self.request_with_role('/review/delete/{}'.format('test'),
            method='DELETE')
        self.check_error(resp, 'REVIEW_NOT_FOUND')

        # confirming no reviews were deleted
        num_after = r.table(TABLE).count().run(self.rdb)
        self.assertEqual(num_before, num_after)


    def test_list_success(self):
        """ Test that reviews that are unapproved are returned """
        # creating reviews
        reviews_list = [
            {'company': 'test1', 'rating':5, 'submitter': 'tester1'},
            {'company': 'test2', 'rating':2, 'submitter': 'tester2'},
            {'company': 'test3', 'rating':8, 'submitter': 'tester3'},
        ]
        for review in reviews_list:
            resp = self.request_with_role('/review/create/123',
                method='POST',
                data=json.dumps(review))
            self.assertEqual(resp.status_code, 201)

        resp = self.request_with_role('review/list',
            method='GET')
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.data)

        # make sure the list at the very least has as many as we created
        self.assertGreaterEqual(resp_data['count'], len(reviews_list))

        # checking that all created reviews were returned
        returned_list = resp_data['data']
        for review in returned_list:
            self.assertFalse(review['approved'])
            del review['id']
            del review['approved']
        for review in reviews_list:
            self.assertIn(review, returned_list)


if __name__ == '__main__':
    unittest.main()

