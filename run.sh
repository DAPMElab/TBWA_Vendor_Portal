#!/bin/bash

sudo service rethinkdb start

source config/settings.dev
cd src
python app.py

sudo service rethinkdb stop

