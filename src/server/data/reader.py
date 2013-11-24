
import rethinkdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import csv
from sys import exit
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
    """
    Sets up the database from scratch
    Will allow the user to execute whether or not the database has already
    been instantiated.
    @return: a set of tables that were added to the specified database
    """
    creations = set()   # set of tables created
    try:
        with rethinkdb.connect(host=rdb_host, port=rdb_port) as conn:
            db_list = rethinkdb.db_list().run(conn)
            if rdb_name not in db_list:
                rethinkdb.db_create(rdb_name).run(conn) # create the db
                print 'Database added'

            conn.use(rdb_name)  # make default db connection
            # find tables that still need to be added then add & populate them
            tbl_list = rethinkdb.db(rdb_name).table_list().run(conn)
            tbl_to_add = ((k, v) for k, v in datasets.items() if k not in tbl_list)
            for (name, path) in tbl_to_add:
                rethinkdb.table_create(name).run(conn)
                rethinkdb.table(name).insert(get_data(name, path)).run(conn)
                print "'{}' table created and populated.".format(name)
                creations.add(name)

    except RqlRuntimeError, e:
        print e
        exit(1)
    
    return creations

