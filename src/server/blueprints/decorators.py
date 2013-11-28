
from functools  import wraps
from config     import make_error
from flask      import session


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return make_error(err='ADMIN_REQUIRED')
        return f(*args, **kwargs)
    return decorated_function

