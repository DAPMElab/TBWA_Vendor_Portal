#!/bin/bash

sudo service rethinkdb start

source config/settings.dev
cd src/server
nosetests

exit 0

