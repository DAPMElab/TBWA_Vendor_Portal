
from flask import Blueprint, request, g, session, make_response
from rethinkdb.errors import RqlRuntimeError
from config import make_error
import json
import rethinkdb as r

review_bp = Blueprint('review_blueprint', __name__)
TABLE = 'reviews'

"""
Handles HTTP requests concerning reveiws made by employees that need to be
approved by an admin.
"""

@review_bp.route('/create/<uid>', methods=['POST'])
def create(uid):
    """ Creates a company review that will set in the approval queue

        @param uid: uid of the company being reviewed
        @json_format: {'data': <review obj>}
    """
    review = json.loads(request.data)
    review['approved'] = False
    outcome = r.table(TABLE).insert(review).run(g.rdb_conn)

    if outcome['inserted'] == 1:
        return make_response(json.dumps({
            'message'   : 'review created',
            'uid'       : outcome['generated_keys'][0]
        }), 201)
    else:
        return make_error(err='REVIEW_NOT_CREATED')


# requires admin
@review_bp.route('/approve/<uid>', methods=['POST'])
def approve(uid):
    """ Removes a review from the queue and links it to the company. """
    outcome = r.table(TABLE).get(uid).update({'approved': True}).run(g.rdb_conn)
    
    if outcome['replaced'] == 1:
        return make_response(json.dumps({
            'message'   : 'review approved'
        }), 200)
    else:
        return make_error(err='REVIEW_APPROVAL_FAILURE')


# requires admin
@review_bp.route('/get/<uid>', methods=['GET'])
def get(uid):
    """ Returns all info for one exact review """
    review = r.table(TABLE).get(uid).pluck(
        'company', 'submitter', 'rating', 'comments', 'approved'
    ).run(g.rdb_conn)

    if review:
        return make_response(json.dumps({
            'message'   : 'reivew found',
            'data'      : review
        }), 200)
    else:
        return make_error(err='REVIEW_NOT_FOUND')


# requires admin
@review_bp.route('/edit/<uid>', methods=['PATCH'])
def edit(uid):
    """ Edits the info for an exact review """
    pass


# requires admin
@review_bp.route('/delete/<uid>', methods=['DELETE'])
def delete(uid):
    """ Removes a review from the queue """
    # use 204
    pass


# requires admin
@review_bp.route('/list', methods=['GET'])
def list():
    """ Returns all reviews that have not yet been approved """
    pass


