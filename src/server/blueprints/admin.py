
from flask              import Blueprint, request, g, session, \
    make_response, render_template, flash, redirect
from rethinkdb.errors   import RqlRuntimeError
from datetime           import datetime
from copy               import deepcopy
from config             import make_error
from decorators         import admin, has_data
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
@has_data
def create():
    """ Creates a new admin with the data passed in """
    admin_data = request.get_json(cache=True)['data']

    # verifying data
    # TODO: think about more redudant data checking
    for key, type in admin_model.items():
        if key not in admin_data:
            return make_error(err='ADMIN_DATA_NEEDED')

    if False: # TODO: add email validator
        return make_error(err='IMPROPER_EMAIL')

    # confirming matching passwords
    if admin_data['password'] != admin_data['repeat_password']:
        return make_error(err='PASSWORDS_UNMATCHED')

    # hashing password & deleting repeat
    hashed_pass = sha256_crypt.encrypt(admin_data['password'])
    admin_data['password'] = hashed_pass
    del admin_data['repeat_password']
    
    # fail if email in use
    matches = [x for x in (r.table('admin')
            .filter({'email': admin_data['email']})
            .run(g.rdb_conn))]
    if len(matches) > 0:
        return make_error(err='EMAIL_IN_USE')

    # creating admin in db
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
    """ Checks for an existing admin and responds accordingliy """
    login_data = request.form
    email = login_data.get('email', default=None)
    password = login_data.get('password', default=None)

    if not email or not password:
        flash('Please enter an email and password')
        return render_template('admin_signin.html')

    # look for the specified admin
    db_admin = [x for x in (r.table('admin')
            .filter({'email': email})
            .run(g.rdb_conn))]

    if not db_admin:    # return ERR if the admin does not exist
        #return make_error(err='ADMIN_DNE')  
        flash('Admin does not exist')
        return render_template('admin_signin.html')
    else:
        db_admin = db_admin[0]

    # check password w/ hash
    if not sha256_crypt.verify(password, db_admin['password']):
        #return make_error(err='INCORRECT_PASSWORD')
        flash('Incorrect password')
        return render_template('admin_signin.html')
    
    # "log" them in
    session['role'] = 'admin'
    session['email'] = db_admin['email']

    #return make_response(json.dumps({
    #    'message': 'logged in'
    #}), 201)

    return redirect('/admin')


