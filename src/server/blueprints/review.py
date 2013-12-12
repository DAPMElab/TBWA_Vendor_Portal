
from flask              import Blueprint, request, g, make_response
from rethinkdb.errors   import RqlRuntimeError
from config             import make_error
from decorators         import admin, has_data
import rethinkdb as r
import json

review_bp   = Blueprint('review_blueprint', __name__)
TABLE       = 'reviews'

"""
Handles HTTP requests concerning reviews made by employees that need to be
approved by an admin.
"""


@review_bp.route('/create/<uid>', methods=['POST'])
@has_data
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


@review_bp.route('/approve/<uid>', methods=['POST'])
@admin
def approve(uid):
    """ Removes a review from the queue and links it to the company. """
    outcome = r.table(TABLE).get(uid).update({'approved': True}).run(g.rdb_conn)
    
    if outcome['replaced'] == 1:
        return make_response(json.dumps({
            'message'   : 'review approved'
        }), 200)
    else:
        return make_error(err='REVIEW_APPROVAL_FAILURE')


@review_bp.route('/get/<uid>', methods=['GET'])
@admin
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


@review_bp.route('/edit/<uid>', methods=['PATCH'])
@admin
@has_data
def edit(uid):
    updated_review = request.get_json(cache=True)

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


@review_bp.route('/delete/<uid>', methods=['DELETE'])
@admin
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


@review_bp.route('/list', methods=['GET'])
@admin
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

