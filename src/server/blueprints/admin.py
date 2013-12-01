
from flask              import Blueprint, request, g, session, make_response
from rethinkdb.errors   import RqlRuntimeError
from datetime           import datetime
from copy               import deepcopy
from config             import make_error
from decorators         import admin
from passlib.hash       import sha256_crypt
from email.utils        import parseaddr
import rethinkdb as r
import json


admin_bp   = Blueprint('admin_blueprint', __name__)
TABLE       = 'admin'

"""
Handles HTTP requests concerning creation and management of admins
"""


admin_model = {
    'email': str,
    'password': str,
    'repeat_password': str
}


@admin_bp.route('/create', methods=['POST'])
def create():
    """ Creates a new admin with the data passed in """
    admin_data = json.loads(request.data)['data']
    print admin_data
    print

    # verifying data
    for key, type in admin_model.items():
        if key not in admin_data:
            return make_error(err='ADMIN_DATA_NEEDED')
        else:
            return make_error(err='ADMIN_DATA_NEEDED')

    # TODO: add email validator
    if False:
        return make_error(err='IMPROPER_EMAIL')

    # confirming matching passwords
    if admin_data['password'] != admin_data['repeat_password']:
        return make_error(err='PASSWORDS_UNMATCHED')

    # hashing password & deleting repeat
    hashed_pass = sha256_crypt.encrypt(admin_data['password'])
    admin_data['password'] = hashed_pass
    del admin_data['repeat_password']
    
    # creating admin
    outcome = r.table(TABLE).insert(admin_data).run(g.rdb_conn)

    if outcome['inserted'] == 1:
        return make_response(json.dumps({
            'message'   : 'admin created',
            'uid'       : outcome['generated_keys'][0]
        }), 201)
    else:
        return make_error(err='ADMIN_NOT_CREATED')


@admin_bp.route('/login', methods=['POST'])
def login():
    pass


