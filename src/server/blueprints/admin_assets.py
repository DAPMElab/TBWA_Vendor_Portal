

from flask  import send_from_directory, Blueprint


admin_assets_bp   = Blueprint('admin_assets_blueprint', __name__)

"""
Handles wrapping HTTP requests concerning assets for the admin page
"""


@admin_assets_bp.route('/js/<path:filename>', methods=['GET'])
def send_js(filename):
    return send_from_directory('../admin/', filename)

@admin_assets_bp.route('/partials/<path:filename>', methods=['GET'])
def send_partial(filename):
    return send_from_directory('../admin/partials/', filename)

@admin_assets_bp.route('/css/<path:filename>', methods=['GET'])
def send_css(filename):
    return send_from_directory('../admin/styles/', filename)

@admin_assets_bp.route('/img/<path:filename>', methods=['GET'])
def send_img(filename):
    return send_from_directory('../admin/img/', filename)


