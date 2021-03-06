
from rethinkdb.errors import RqlRuntimeError
from decorators import admin, has_data
from config import make_error
from flask import Blueprint, request, g, make_response
import rethinkdb as r
import json
import datetime

"""
Handles HTTP requests concerning reviews made by employees that need to be
approved by an admin.
"""


review_bp = Blueprint('review_blueprint', __name__)
TABLE = 'reviews'
C_TABLE = 'companies'

required_fields = [
    'CompanyID',
    'CompanyName',
    'Rating',
]

return_fields = required_fields + [
    'Approved',
    'Reviewer',
]


@review_bp.route('/create/<uid>', methods=['POST'])
@has_data
def create(uid):
    """ Creates a company review that will set in the approval queue

        @param uid: uid of the company being reviewed
        @json_format: {'data': <review obj>}
    """
    review = request.get_json(cache=True)
    review['CompanyID'] = uid
    review['Approved'] = False
    review['Date'] = datetime.date.today().isoformat()
    # add the writer to the review
    review['Reviewer'] = request.headers.get('WTG_mail', 'Anonymous')

    for field in required_fields:
        if field not in review:
            return make_error(err='DATA_NEEDED_FOR_REQUEST')

    r_outcome = (r.table(TABLE)
                 .insert(review)
                 .run(g.rdb_conn))

    if r_outcome['inserted'] == 1:
        return make_response(json.dumps({
            'message': 'review created',
            'uid':  r_outcome['generated_keys'][0]
        }), 201)
    else:
        return make_error(err='REVIEW_NOT_CREATED')


@review_bp.route('/approve/<uid>', methods=['POST'])
@admin
def approve(uid):
    """ Removes a review from the queue and links it to the company. """
    try:
        outcome = (r.table(TABLE)
                    .get(uid)
                    .update({
                        'Approved': True
                    }, return_vals=True).run(g.rdb_conn))
    except RqlRuntimeError:
        return make_error(err='REVIEW_APPROVAL_FAILURE')

    cid = outcome['old_val']['CompanyID']
    rid = outcome['old_val']['id']
    c_outcome = (r.table(C_TABLE)
                 .get(cid)
                 .update({
                     'ReviewIds': r.row['ReviewIds'].set_insert(rid)
                 }).run(g.rdb_conn))

    if c_outcome['replaced'] == 1:
        return make_response(json.dumps({
            'message': 'review approved'
        }), 200)
    else:
        return make_error(err='REVIEW_APPROVAL_FAILURE')


@review_bp.route('/get/<uid>', methods=['GET'])
@admin
def get(uid):
    """ Returns all info for one exact review """
    try:
        review = r.table(TABLE).get(uid).pluck(*return_fields).run(g.rdb_conn)

        return make_response(json.dumps({
            'message': 'review found',
            'data': review
        }), 200)
    except RqlRuntimeError:
        return make_error(err='REVIEW_NOT_FOUND')


@review_bp.route('/edit/<uid>', methods=['PATCH'])
@admin
@has_data
def edit(uid):
    updated_review = request.get_json(cache=True)
    try:
        outcome = r.table(TABLE).get(uid).update(updated_review).run(g.rdb_conn)
        return make_response(json.dumps({
            'message': 'review updated'
        }), 200)
    except RqlRuntimeError:
        return make_error(err='REVIEW_NOT_FOUND')


@review_bp.route('/delete/<uid>', methods=['DELETE'])
@admin
def delete(uid):
    """ Removes a review from the queue """
    try:
        outcome = r.table(TABLE).get(uid).delete().run(g.rdb_conn)
        return make_response(json.dumps({
            'message': 'review deleted'
        }), 202)
    except RqlRuntimeError:
        return make_error(err='REVIEW_NOT_FOUND')


@review_bp.route('/list', methods=['GET'])
@admin
def list():
    """ Returns all reviews that have not yet been approved """
    try:
        outcome = r.table(TABLE).filter({'Approved': False}).run(g.rdb_conn)
        reviews = [x for x in outcome]

        return make_response(json.dumps({
            'data': reviews,
            'count': len(reviews)
        }), 200)

    except RqlRuntimeError:
        return make_error(err='DATABASE_ERROR')
