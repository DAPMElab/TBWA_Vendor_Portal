
from flask              import Flask, make_response, g
from rethinkdb.errors   import RqlDriverError
from data               import setup_db
import rethinkdb
import argparse


app = Flask(__name__)
app.config.from_object('config.flask_config')


@app.before_request
def before_request():
    """ Add a rethinkdb connection to g before each request """
    try:
        g.rdb_conn = rethinkdb.connect(
            host    = app.config['RDB_HOST'],
            port    = app.config['RDB_PORT'],
            db      = app.config['RDB_DB']
        )
    except RqlDriverError:
        return ERR('NO_DB_CONN')


@app.teardown_request
def teardown_request(exception):
    """ Close the new rethinkdb connection after each request """
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


""" data routes """
from blueprints import data_bp
app.register_blueprint(data_bp)


@app.route('/', methods=['GET'])
def home():
    """ Return the html seed file with linked JS """
    return make_response('hello world!')


def parse_cli_args():
    """ Parse CLI arguments """
    parser = argparse.ArgumentParser(
        description='take in CLI arguments for the company API')

    parser.add_argument('--setup', dest='run_setup', action='store_const',
        const=True, default=False)

    return parser.parse_args()


if __name__ == '__main__':
    cli_args = parse_cli_args()

    if cli_args.run_setup:
        # create tables and insert data
        setup_db(
            rdb_host    = app.config['RDB_HOST'],
            rdb_port    = app.config['RDB_PORT'],
            rdb_name    = app.config['RDB_DB']
        )

    app.run(host='0.0.0.0')   # run app if not setting up

