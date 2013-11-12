#!/bin/bash

sudo service rethinkdb start

source config/settings.dev
nosetests

sudo service rethinkdb stop

