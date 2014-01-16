#!/bin/bash

sudo service rethinkdb start

sudo pip install flask
sudo pip install gunicorn
sudo pip install rethinkdb
sudo pip install passlib

source config/settings.prod
cd src/server
gunicorn app:app

exit 0 

