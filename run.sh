#!/bin/bash

sudo service rethinkdb start

source config/settings.dev
cd src/server
python app.py --setup

exit 0 

