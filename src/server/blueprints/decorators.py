
from functools  import wraps
from config     import make_error
from flask      import session, request


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return make_error(err='ADMIN_REQUIRED')
        return f(*args, **kwargs)
    return decorated_function


def has_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        json = request.get_json(
            force=True,
            silent=True,
            cache=True)
        if not json:
            return make_error(err='DATA_NEEDED_FOR_REQUEST')
        return f(*args, **kwargs)
    return decorated_function


