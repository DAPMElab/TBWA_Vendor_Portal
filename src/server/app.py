
from flask              import Flask, make_response, g, send_from_directory, \
        session, render_template
from rethinkdb.errors   import RqlDriverError
from data               import setup_db
from config.errors      import make_error
from blueprints         import admin
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
        return make_error('NO_DB_CONN')


@app.teardown_request
def teardown_request(exception):
    """ Close the new rethinkdb connection after each request """
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


""" review routes """
from blueprints import review_bp
app.register_blueprint(review_bp, url_prefix='/review')

""" company routes """
from blueprints import company_bp
app.register_blueprint(company_bp, url_prefix='/company')

""" admin routes """
from blueprints import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

""" client asset routes """
from blueprints import client_bp 
app.register_blueprint(client_bp, url_prefix='/client')

""" admin asset routes """
from blueprints import admin_assets_bp 
app.register_blueprint(admin_assets_bp, url_prefix='/admin_asset')


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory('static/', 'favicon.ico')


@app.route('/admin_credentials', methods=['GET'])
def become_admin():
    """ Testing method that adds a cookie to the browser for admin access """
    session['role'] = 'admin'
    return "You're now an admin!", 200


@app.route('/admin', methods=['GET'])
def admin():
    """ Return the html seed file with linked JS """
    if 'role' not in session or session['role'] != 'admin':
        return render_template('admin_signin.html')
    with open(app.config['HOME_PATH']+'/src/admin/base.html') as base:
        return make_response(base.read())


@app.route('/', methods=['GET'])
def home():
    """ Return the html seed file with linked JS """
    with open(app.config['HOME_PATH']+'/src/client/index.html') as base:
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

