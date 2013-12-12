
from flask              import Blueprint, request, g, make_response
from rethinkdb.errors   import RqlRuntimeError
from config             import make_error
from decorators         import admin, has_data
import rethinkdb as r
import json

company_bp   = Blueprint('company_blueprint', __name__)
TABLE       = 'companies'

"""
Handles HTTP requests made by the admin for changing company data
"""

required_company_attributes = [
    'name',
    'website'
]

@company_bp.route('/create', methods=['POST'])
@has_data
def create():
    """ Creates a new company that will be displayed.
    """
    company = request.get_json(cache=True)
    for field in required_company_attributes:
        if field not in company:
            return make_error(err='DATA_NEEDED_FOR_REQUEST')

    outcome = r.table(TABLE).insert(company).run(g.rdb_conn)
    if outcome['inserted'] == 1:
        return make_response(json.dumps({
            'message'   : 'company created',
            'uid'       : outcome['generated_keys'][0]
        }), 201)
    else:
        return make_error(err='COMPANY_NOT_CREATED')
    










