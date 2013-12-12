
from flask import Blueprint, request, g
from rethinkdb.errors import RqlRuntimeError
from config import make_error
import json
import rethinkdb

data_bp = Blueprint('data routes', __name__)


@data_bp.route('/data', methods=['GET'])
def get_all_data():
    """ Returns all the data from the specified dataset """
    try:
        data_cursor = rethinkdb.table('diverse').run(g.rdb_conn)
        data = [row for row in data_cursor]
    except RqlRuntimeError, e:
        return make_error(err='DATASET_NOT_FOUND')

    return json.dumps({'data': data}), 201



