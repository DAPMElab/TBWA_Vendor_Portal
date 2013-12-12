
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


@company_bp.route('/create', methods=['POST'])
@has_data
def create():
    """ Creates a new company that will be displayed.
    """
    company = json.loads(request.data)










