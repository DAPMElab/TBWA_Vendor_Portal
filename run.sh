#!/bin/bash

sudo service rethinkdb start

source config/settings.dev
cd src
python app.py --setup

sudo service rethinkdb stop

exit 0 

