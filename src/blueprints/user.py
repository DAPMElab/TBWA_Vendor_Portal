
from flask import Blueprint, request, g, session
from rethinkdb.errors import RqlRuntimeError
from config import make_error
import json
import rethinkdb

user_bp = Blueprint('user routes', __name__)

#NOTE: none of this may be necessary depending on how we do auth

@user_bp.route('/create', methods=['POST'])
def create():
    """ Creates a user from the json data passed in. The user is saved in the
        'user' table of the db. """
    data = json.loads(request.data)
    pass


@user_bp.route('/get/<uid>', methods=['GET'])
def get(uid):
    """ Returns the user corresponding to 'uid' """
    pass


@user_bp.route('/update/<uid>', methods=['PATCH'])
def update(uid):
    """ Updates the data of the user corresponding to 'uid'. """
    data = json.loads(request.data)
    pass


@user_bp.route('/delete/<uid>', methods=['DELETE'])
def delete(uid):
    """ Deletes the user corresponding to 'uid'."""
    #TODO: decided if implementing lazy deletion is worthwhile
    data = json.loads(request.data)
    pass


