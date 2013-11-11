
from flask import Blueprint, request, g
from rethinkdb.errors import RqlRuntimeError
from config import make_error
import json
import rethinkdb

data_bp = Blueprint('data routes', __name__)


@data_bp.route('/<dataset>')
def get_all_data(dataset):
    """ Returns all the data from the specified dataset """
    dataset = str(dataset)
    print dataset
    try:
        data = [row for row in rethinkdb.table(dataset).run(g.rdb_conn)]
    except RqlRuntimeError, e:
        return make_error('DATASET_NOT_FOUND')

    return json.dumps({'data': data}), 201

