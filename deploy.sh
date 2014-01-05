#!/bin/bash

sudo service rethinkdb start

source config/settings.prod
cd src/server
gunicorn app:app

exit 0 

