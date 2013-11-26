
from flask import Blueprint, request, g, session
from rethinkdb.errors import RqlRuntimeError
from config import make_error
import json
import rethinkdb

review_bp = Blueprint('review_blueprint', __name__)

"""
Handles HTTP requests concerning reveiws made by employees that need to be
approved by an admin.
"""

@review_bp.route('/create/<uid>', methods=['POST'])
def create(uid):
    """ Creates a company review that will set in the approval queue
        @param uid: uid of the company being reviewed """
    pass


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


@review_bp.route('/delete/<uid>', methods['DELETE'])
def delete(uid):
    """ Removes a review from the queue """
    # requires admin
    pass


@review_bp.route('/list', methods=['GET'])
def list():
    """ Returns all reviews that have not yet been approved """
    # requires admin
    pass


