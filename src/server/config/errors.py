
import json
from flask import make_response

errors = {
    'english': {
        'DEFAULT': {
            'message': 'unspecified error on server',
            'status_code': 500
        },
        'NO_DB_CONN': {
            'message': 'a database connection could not be established',
            'status_code': 503
        },
        'DATASET_NOT_FOUND': {
            'message': 'that dataset could not be found',
            'status_code': 404
        },
        'DATABASE_ERROR': {
            'message': 'there was an error accessing our databse',
            'status_code': 503
        },
        'NOT_LOGGED_IN': {
            'message': "sorry, you're not logged in yet",
            'status_code': 401
        },
        # REVIEWS
        'REVIEW_NOT_CREATED': {
            'message': 'error creating review',
            'status_code': 400
        },
        'REVIEW_APPROVAL_FAILURE' : {
            'message': 'error updating review',
            'status_code': 400
        },
        'REVIEW_NOT_FOUND': {
            'message': 'review was not found',
            'status_code': 404
        }
    }
}


def make_error(err='DEFAULT', language='english'):
    """
    Forms a response object based off of the passed in error name.
    Returns 500 when the specified error is not found.
    """
    json_data, code = construct_err(err_name=err, err_language=language)
    return make_response(json_data, code)


def construct_err(err_name='DEFAULT', err_language='english'):
    """
    Forms a json object based off of the passed in error name.
    Returns the json & status_code
    """
    if err_language not in errors.keys():
        err_language = 'english'
    if err_name not in errors[err_language].keys():
        err_name = 'DEFAULT'

    error_obj = errors[err_language][err_name]

    return json.dumps({
        'message': error_obj['message'],
        'status_code': error_obj['status_code']
    }), error_obj['status_code']

