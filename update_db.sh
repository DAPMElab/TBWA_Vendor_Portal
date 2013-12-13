#!/bin/sh

rethinkdb import -c localhost:28015 -f src/server/data/assets/tbwa/companies.json --table TBWA.companies --force

