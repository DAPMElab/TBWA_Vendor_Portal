
import rethinkdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import csv
import os
this_dir = os.path.dirname(__file__)

data_paths = {
    'diverse': os.path.join(this_dir, 'assets/tbwa/diverse_vendors_list.csv')
}


def get_data(dataset, path_to_data=None):
    """ Returns the columns and a list of data with the specified dataset """
    # TODO: redesign when db is implemented to insert row by row

    if not path_to_data:
        if dataset not in data_paths:
            raise Exception('Invalid dataset')
        else:
            path_to_data = data_paths[dataset]

    with open(path_to_data, 'rb') as f:
        data_reader = csv.reader(f)
        columns = data_reader.next()

        data = []
        for row in data_reader:
            obj = {}
            for index, col in enumerate(columns):
                obj[col] = row[index]
            data.append(obj)

    return data


def setup_db(rdb_host, rdb_port, rdb_name):
    """ Sets up the database from scratch """
    with rethinkdb.connect(host=rdb_host, port=rdb_port) as conn:
        try:
            rethinkdb.db_create(rdb_name).run(conn) # create the db
            for dataset in data_paths: # create a table for each dataset
                rethinkdb.db(rdb_name).table_create(dataset).run(conn)
                rethinkdb.db(rdb_name).table(dataset).insert(get_data(dataset)).run(conn)

            print 'Database created!'

            # TODO: insert all the data

        except RqlRuntimeError, e:
            print e
            print 'Database already instantiated, run without --setup'


