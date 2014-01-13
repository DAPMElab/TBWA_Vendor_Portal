
import rethinkdb
from rethinkdb.errors import RqlRuntimeError
import json
from sys import exit
import os
this_dir = os.path.dirname(__file__)

if os.environ['DEPLOY'] == 'TRUE' or os.environ['TESTING'] == 'TRUE':
    data_paths = {'companies': os.path.join(this_dir,
                                            'assets/tbwa/companies.json')}
    application_tables = ['admin', 'reviews']
else:
    data_paths = {}
    application_tables = ['admin', 'reviews', 'companies']


def setup_db(rdb_host, rdb_port, rdb_name,
             datasets=data_paths,               # datasets to be loaded
             app_tables=application_tables):    # tables to be created
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
                rethinkdb.db_create(rdb_name).run(conn)  # create the db
                print 'Database added'
            conn.use(rdb_name)  # make default db connection

            # find tables that still need to be added then add & populate them
            tbl_list = [x for x in
                        rethinkdb.db(rdb_name).table_list().run(conn)]

            tbl_to_add = [(k, v) for k, v
                          in datasets.items() if k not in tbl_list]
            print "TBL_TO_ADD"
            print tbl_to_add
            for (name, path) in tbl_to_add:
                rethinkdb.table_create(name).run(conn)
                try:
                    with open(path, 'r') as f:
                        (rethinkdb
                            .table(name)
                            .insert(json.loads(f.read()))
                            .run(conn))
                except IOError:
                    raise Exception('Invalid Dataset')
                print "'{}' table created and populated.".format(name)
                creations.add(name)

            tbl_to_add = (n for n in app_tables if n not in tbl_list)
            for name in tbl_to_add:
                rethinkdb.table_create(name).run(conn)
                print "'{}' table created and populated.".format(name)
                creations.add(name)

    except RqlRuntimeError, e:
        print e
        exit(1)

    return creations
