#!/bin/bash

sudo service rethinkdb start

source /vagrant/config/settings.dev
cd /vagrant/src/server
python app.py --setup

exit 0 

