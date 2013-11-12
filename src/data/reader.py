
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
    """
    with rethinkdb.connect(host=rdb_host, port=rdb_port) as conn:
        try:
            rethinkdb.db_create(rdb_name).run(conn) # create the db
            print 'Database added'

        except RqlRuntimeError, e:
            message =  e.message.split(' ')
            del message[1]
            if message != [u'Database', u'already', u'exists.']:
                print e
                exit(1)

        conn.use(rdb_name)
        for name, path in datasets.items(): # create a table for each dataset
            try:
                rethinkdb.table_create(name).run(conn)
                rethinkdb.table(name).insert(
                    get_data(name, path)).run(conn)
                print '{} table created.'.format(name)

            except RqlRuntimeError, e:
                message =  e.message.split(' ')
                table = message.pop(1)
                if (message != [u'Table', u'already', u'exists.'] or
                        table.encode('utf-8').replace('`', '') not in datasets):
                    print e
                    exit(1)


