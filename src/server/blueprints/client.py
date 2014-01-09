
from flask  import send_from_directory, Blueprint


client_bp   = Blueprint('client_blueprint', __name__)

"""
Handles wrapping HTTP requests concerning assets for the client page
"""


@client_bp.route('/<path:filename>', methods=['GET'])
def send_js(filename):
    return send_from_directory('../client/', filename)


