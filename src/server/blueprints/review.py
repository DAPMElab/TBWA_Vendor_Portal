
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
    outcome = r.table(TABLE).insert(review).run(g.rdb_conn)
    print outcome
    if outcome['inserted'] == 1 and outcome['errors'] == 0:
        return make_response(json.dumps({
            'message': 'review created'
        }), 200)
    else:
        return make_response(json.dumps({
            'message': 'error creating review'
        }), 400)


@review_bp.route('/approve', methods=['POST'])
def approve():
    """ Removes a review from the queue and links it to the company. """
    # requires admin
    pass


@review_bp.route('/get/<uid>', methods=['GET'])
def get(uid):
    """ Returns all info for one exact review """
    # requires admin
    pass


@review_bp.route('/edit/<uid>', methods=['PATCH'])
def edit(uid):
    """ Edits the info for an exact review """
    # requires admin
    pass


@review_bp.route('/delete/<uid>', methods=['DELETE'])
def delete(uid):
    """ Removes a review from the queue """
    # requires admin
    pass


@review_bp.route('/list', methods=['GET'])
def list():
    """ Returns all reviews that have not yet been approved """
    # requires admin
    pass


