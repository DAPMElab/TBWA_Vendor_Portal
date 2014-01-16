#!/bin/bash

# make sure to catch the SIGTERM signal
trap : SIGTERM

# set up the environmental variables
source $1
# supervisord will not do this for us

# start rethinkdb
sudo service rethinkdb start

# start the python program in the background
cd /vagrant/src/server
python app.py --setup &
FIND_PID=$!

# wait for the program to finish
wait $FIND_PID

# If the return value from wait was greater than 128,
# it means we caught a SIGTERM
# kill off the python program in that case
if [ $? -gt 128 ]; then
	echo "Stopping tbwa diverse vendor application server"
	kill $FIND_PID
fi
