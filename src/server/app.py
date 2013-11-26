
from flask              import Flask, make_response, g, send_from_directory
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

""" user routes """
from blueprints import user_bp
app.register_blueprint(user_bp)

""" login/logout routes """
from blueprints import client_bp
app.register_blueprint(client_bp)

""" review routes """
from blueprints import review_bp
app.register_blueprint(review_bp, url_prefix='/review')


@app.route('/js/<path:filename>', methods=['GET'])
def send_js(filename):
    return send_from_directory('../client/', filename)

@app.route('/partials/<path:filename>', methods=['GET'])
def send_partial(filename):
    return send_from_directory('../client/partials/', filename)

@app.route('/css/<path:filename>', methods=['GET'])
def send_css(filename):
    return send_from_directory('../client/styles/', filename)

@app.route('/', methods=['GET'])
def home():
    """ Return the html seed file with linked JS """
    with open('../client/index.html') as base:
        return make_response(base.read())


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
        setup_db(   # create tables and insert data
            rdb_host    = app.config['RDB_HOST'],
            rdb_port    = app.config['RDB_PORT'],
            rdb_name    = app.config['RDB_DB']
        )

    # remove the host setting if running locally, not in Vagrant
    app.run(host='0.0.0.0')

