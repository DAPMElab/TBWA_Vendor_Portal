
import simplejson
from flask import make_reponse

errors = {
    'english': {
        'NO_DB_CONN': {
            'message': 'a database connection could not be established',
            'code': 503
        },
        'DEFAULT': {
            'message': 'unspecified error on server',
            'code': 500
        }
    }
}


def make_error(err_name, language='english'):
    """
    Forms a response object based off of the passed in error name.
    Returns 500 when the specified error is not found.
    """
    try:
        error_obj = errors[language][err_name]
    except KeyError:
        error_obj = errors[language]['DEFAULT']

    return flask.make_reponse(
        simplejson.dumps({'message': error_obj['message']}), 
        error_obj['code']
    )

