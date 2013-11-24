
from os import environ as env
import sys

try:
    # rethinkdb settings
    RDB_HOST = env['RDB_HOST']
    RDB_PORT = env['RDB_PORT']
    RDB_DB = env['RDB_DB']
    
    # flask settings
    DEBUG = False
    if env['FLASK_DEBUG'] == 'TRUE':
        DEBUG = True

except KeyError:
    """ Throw an error and exit if any settings are missing """
    print ("Some of your settings aren't in the environment.\n" +
        "You probably need to source your config file.\n" + 
        "`source config/<your settings file>.prod`")
    sys.exit(1)


