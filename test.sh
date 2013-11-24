#!/bin/bash

sudo service rethinkdb start

source config/settings.dev
cd src/server
nosetests

sudo service rethinkdb stop

exit 0

