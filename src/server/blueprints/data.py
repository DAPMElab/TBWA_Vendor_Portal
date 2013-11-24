
from flask import Blueprint, request, g
from rethinkdb.errors import RqlRuntimeError
from config import make_error
import json
import rethinkdb

data_bp = Blueprint('data routes', __name__)


@data_bp.route('/<dataset>', methods=['GET'])
def get_all_data(dataset):
    """ Returns all the data from the specified dataset """
    dataset = str(dataset)
    try:
        data = [row for row in rethinkdb.table(dataset).run(g.rdb_conn)]
    except RqlRuntimeError, e:
        return make_error(err='DATASET_NOT_FOUND')

    return json.dumps({'data': data}), 201


@data_bp.route('/datasets', methods=['GET'])
def return_dataset_names():
    """ Return all the names of all datasets in the database """
    try:
        dataset_list = [x for x in rethinkdb.table_list().run(g.rdb_conn)]
    except RqlRuntimeError, e:
        return make_error(err='DATABASE_ERROR')
    
    return json.dumps({'data': dataset_list}), 201



