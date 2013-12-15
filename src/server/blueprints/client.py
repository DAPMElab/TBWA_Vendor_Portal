
from flask  import send_from_directory, Blueprint


client_bp   = Blueprint('client_blueprint', __name__)

"""
Handles wrapping HTTP requests concerning assets for the client page
"""


@client_bp.route('/js/<path:filename>', methods=['GET'])
def send_js(filename):
    return send_from_directory('../client/', filename)

@client_bp.route('/partials/<path:filename>', methods=['GET'])
def send_partial(filename):
    return send_from_directory('../client/partials/', filename)

@client_bp.route('/css/<path:filename>', methods=['GET'])
def send_css(filename):
    return send_from_directory('../client/styles/', filename)

@client_bp.route('/img/<path:filename>', methods=['GET'])
def send_img(filename):
    return send_from_directory('../client/img/', filename)


