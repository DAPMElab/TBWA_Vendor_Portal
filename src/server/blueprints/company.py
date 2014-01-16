
from flask              import Blueprint, request, g, make_response
from rethinkdb.errors   import RqlRuntimeError
from config             import make_error
from decorators         import admin, has_data
import rethinkdb as r
import json

company_bp   = Blueprint('company_blueprint', __name__)
TABLE       = 'companies'
R_TABLE     = 'reviews'

"""
Handles HTTP requests made by the admin for changing company data
"""

required_company_attributes = [
    'Name',
    'URL',
]
return_company_attribute = [
    'Name',
    'URL',
    'DBA',
    'id',
    'ReviewIds',
    'Categories',
    'PhysicalAddress',
]

@company_bp.route('/create', methods=['POST'])
@admin
@has_data
def create():
    """ Creates a new company that will be displayed.
    """
    company = request.get_json(cache=True)
    for field in required_company_attributes:
        if field not in company:
            return make_error(err='DATA_NEEDED_FOR_REQUEST')

    company['ReviewIds'] = []

    outcome = r.table(TABLE).insert(company).run(g.rdb_conn)
    print outcome
    if outcome['inserted'] == 1:
        return make_response(json.dumps({
            'message'   : 'company created',
            'uid'       : outcome['generated_keys'][0]
        }), 201)
    else:
        return make_error(err='COMPANY_NOT_CREATED')


@company_bp.route('/get/<uid>', methods=['GET'])
def get(uid):
    """ Returns all information for a specific company """
    try:
        company = (r.table(TABLE).get(uid).do(
            lambda comp : r.expr({
                'Company': comp,
                'Reviews': {
                    'Messages'  : r.table(R_TABLE).filter({
                        'Approved': True,
                        'Company': comp['id']
                    }).coerce_to('array'),
                    'Sum'       : r.table(R_TABLE).filter({
                        'Approved': True,
                        'Company': comp['id']
                    }).map(
                        lambda rev: rev['Rating']
                    ).reduce(
                        lambda a, b : a+b, 0
                    )
                }
            })
        )).run(g.rdb_conn)
    except RqlRuntimeError, e:
        print e
        return make_error(err='COMPANY_NOT_FOUND')


    if company:
        return make_response(json.dumps({
            'message'   : 'company found',
            'data'      : company
        }), 200)
    return make_error(err='COMPANY_NOT_FOUND')


@company_bp.route('/list/<path:info>',                methods=['GET'])
@company_bp.route('/list', defaults={'info':None},    methods=['GET'])
def list(info):
    """ 2 paths, /list & /list/all
    /list:  For use on the main search page, returns limited attributes as well
            as the review data like average
    """

    try:
        if not info or info != 'all':       # /list
            # TODO: refactor!
            cursor = (r.table(TABLE).map(
                lambda comp : r.expr({
                    'Company': comp.pluck(
                        *return_company_attribute
                    ),
                    'Reviews': {
                        'Count'     : r.table(R_TABLE).filter({
                            'Approved': True,
                            'Company': comp['id']
                        }).count(),
                        'Sum'       : r.table(R_TABLE).filter({
                            'Approved': True,
                            'Company': comp['id']
                        }).map(
                            lambda rev: rev['Rating']
                        ).reduce(
                            lambda a, b : a+b, 0
                        )
                    }
                })
            )).run(g.rdb_conn)

            # resolve average
            companies = []
            for c in cursor:
                if c['Reviews']['Count']:
                    c['Company']['AverageReview'] = c['Reviews']['Sum']
                    c['Company']['AverageReview'] /= c['Reviews']['Count']
                else:
                    c['Company']['AverageReview'] = None
                # clean up
                del c['Reviews']
                companies.append(c['Company'])

        else:   # /list/all
            cursor = (r.table(TABLE)
                    .run(g.rdb_conn))
            companies = [x for x in cursor]

        return make_response(json.dumps({
            'message'   : 'company list',
            'count'     : len(companies),
            'data'      : companies
        }), 200)
    except RqlRuntimeError, e:
        print e
        return make_error(err='DATABASE_ERROR')


@company_bp.route('/edit/<uid>', methods=['PATCH'])
@admin
@has_data
def edit(uid):
    """ Updates all fields passed in on the company object """
    updated_company = request.get_json(cache=True)

    #TODO: think about logging edits in the obj
    try:
        outcome = r.table(TABLE).get(uid).update(updated_company).run(g.rdb_conn)
        if outcome['skipped']:
            return make_error(err='COMPANY_NOT_FOUND')

        return make_response(json.dumps({
            'message'   : 'company updated'
        }), 200)
    except RqlRuntimeError:
        return make_error(err='DATABASE_ERROR')


@company_bp.route('/delete/<uid>', methods=['DELETE'])
@admin
def delete(uid):
    """ Deletes a company object based on id """

    try:
        outcome = r.table(TABLE).get(uid).delete().run(g.rdb_conn)
        if outcome['skipped']:
            return make_error(err='COMPANY_NOT_FOUND')

        return make_response(json.dumps({
            'message'   : 'company deleted'
        }), 202)
    except RqlRuntimeError:
        return make_error(err='DATABASE_ERROR')


