
from flask import Blueprint, request, g, session
from rethinkdb.errors import RqlRuntimeError
from config import make_error
import json
import rethinkdb

client_bp = Blueprint('client routes', __name__)


@client_bp.route('/login', methods=['POST'])
def login():
    """ Verifies login info with the db and then creates a cookie for the
        user """
    #TODO: figure out details on how TBWA wants to do this
    # for now, mocks a response
    data = json.loads(request.data)
    print data
    session['username'] = 'tester'
    session['admin'] = False
    return make_response(json.dumps({
        'message': 'Logged in!'
    }), 200)


@client_bp.route('/logout', methods=['POST'])
def logout():
    """ Clears the client's cookie """
    session.clear()
    return make_response(json.dumps({
        'message': 'Logged out!'
    }), 200)


@client_bp.route('/session')
def get_session():
    """
    Returns json w/ unique identifier
    """
    if 'username' in session:
        return JSON.dumps({
            'username'  : session['username'],
            'admin'     : session['admin']
        }), 200
    return make_error(err='NOT_LOGGED_IN')

