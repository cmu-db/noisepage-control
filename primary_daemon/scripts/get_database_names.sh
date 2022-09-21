#!/bin/bash

##################################  NOTE  ##################################
#   This script gets all database names
#       $ sudo -u postgres scripts/get_database_names.sh 10000 postgres
###############################################################################

##############################  Configurations  ##############################

DATABASE_PORT=$1
PG_USERNAME=$2

###############################################################################

sudo -u postgres bash -c "echo \"SELECT datname FROM pg_database WHERE datistemplate = false;\" | psql -p ${DATABASE_PORT} --username ${PG_USERNAME}"
