
from flask import Blueprint, request, g, session, make_response
from rethinkdb.errors import RqlRuntimeError
from datetime import datetime
from copy import deepcopy
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
    try:
        review = r.table(TABLE).get(uid).pluck(
            'company', 'submitter', 'rating', 'comments', 'approved'
        ).run(g.rdb_conn)

        return make_response(json.dumps({
            'message'   : 'review found',
            'data'      : review
        }), 200)
    except RqlRuntimeError:
        return make_error(err='REVIEW_NOT_FOUND')


# requires admin
@review_bp.route('/edit/<uid>', methods=['PATCH'])
def edit(uid):
    """ Edits the info for an exact review """
    try:
        updated_review = json.loads(request.data)
    except ValueError:
        return make_error(err='DATA_NEEDED_FOR_REQUEST')

    #TODO: think about logging edits in the obj
    try:
        outcome = r.table(TABLE).get(uid).update(updated_review).run(g.rdb_conn)
        if outcome['skipped']:
            return make_error(err='REVIEW_NOT_FOUND')

        return make_response(json.dumps({
            'message'   : 'review updated'
        }), 200)
    except RqlRuntimeError:
        return make_error(err='DATABASE_ERROR')


# requires admin
@review_bp.route('/delete/<uid>', methods=['DELETE'])
def delete(uid):
    """ Removes a review from the queue """
    try:
        outcome = r.table(TABLE).get(uid).delete().run(g.rdb_conn)
        if outcome['skipped']:
            return make_error(err='REVIEW_NOT_FOUND')

        return make_response(json.dumps({
            'message'   : 'review deleted'
        }), 202)
    except RqlRuntimeError:
        return make_error(err='DATABASE_ERROR')


# requires admin
@review_bp.route('/list', methods=['GET'])
def list():
    """ Returns all reviews that have not yet been approved """
    try:
        outcome = r.table(TABLE).filter({'approved':False}).run(g.rdb_conn)
        reviews = [x for x in outcome]

        return make_response(json.dumps({
            'data': reviews,
            'count': len(reviews)
        }), 200)

    except RqlRuntimeError:
        return make_error(err='DATABASE_ERROR')

