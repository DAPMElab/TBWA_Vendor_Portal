
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
            'message': 'there was an error accessing our database',
            'status_code': 503
        },
        'NOT_LOGGED_IN': {
            'message': "sorry, you're not logged in yet",
            'status_code': 401
        },
        'DATA_NEEDED_FOR_REQUEST': {
            'message': 'this endpoint requires data to operate',
            'status_code': 400
        },
        'PASSWORDS_UNMATCHED': {
            'message': 'passwords passed do not match',
            'status_code': 400
        },
        'INCORRECT_PASSWORD': {
            'message': 'password incorrect',
            'status_code': 401
        },
        'IMPROPER_EMAIL': {
            'message': 'email is invalid',
            'status_code': 400
        },
        'EMAIL_IN_USE': {
            'message': 'email already in use',
            'status_code': 400
        },
        'MISSING_LOGIN_DATA': {
            'message': 'an email and passowrd are needed for login',
            'status_code': 400
        },
        # COMPANIES
        'COMPANY_NOT_CREATED': {
            'message': 'error creating compay',
            'status_code': 400
        },
        'COMPANY_NOT_FOUND': {
            'message': 'company was not found',
            'status_code': 404
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
        },

        # ADMIN
        'ADMIN_REQUIRED': {
            'message': 'this endpoint requires admin credentials',
            'status_code': 403
        },
        'ADMIN_DATA_NEEDED': {
            'message': 'data is missing to create an admin',
            'status_code': 400
        },
        'ADMIN_NOT_CREATED': {
            'message': 'error creating admin',
            'status_code': 400
        },
        'ADMIN_DNE': {
            'message': 'the specified admin does not exist',
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

