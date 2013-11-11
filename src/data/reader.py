
import rethinkdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import csv
import os
this_dir = os.path.dirname(__file__)

data_paths = {
    'diverse': os.path.join(this_dir, 'assets/tbwa/diverse_vendors_list.csv')
}


def get_data(dataset, path_to_data):
    """ Returns the columns and a list of data with the specified dataset """
    # TODO: redesign when db is implemented to insert row by row
    # so that the whole dataset isn't loaded into memory

    try:
        with open(path_to_data, 'rb') as f:
            data_reader = csv.reader(f)
            columns = data_reader.next()

            data = []
            for row in data_reader:
                obj = {}
                for index, col in enumerate(columns):
                    obj[col] = row[index]
                data.append(obj)

    except IOError:
        raise Exception('Invalid dataset')

    return data


def setup_db(rdb_host, rdb_port, rdb_name, datasets=data_paths):
    """ Sets up the database from scratch """
    with rethinkdb.connect(host=rdb_host, port=rdb_port) as conn:
        try:
            rethinkdb.db_create(rdb_name).run(conn) # create the db
            conn.use(rdb_name)
            for name, path in datasets.items(): # create a table for each dataset
                rethinkdb.table_create(name).run(conn)
                rethinkdb.table(name).insert(
                    get_data(name, path)).run(conn)

        except RqlRuntimeError, e:
            print e
            print 'Database already instantiated, run without --setup'


