#!/bin/bash

service rethinkdb start

source config/settings.dev
cd src
python app.py

service rethinkdb stop

