
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
    pass


@client_bp.route('/logout', methods=['POST'])
def logout():
    """ Clears the client's cookie """
    session.clear()


