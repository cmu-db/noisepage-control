#!/bin/bash

##################################  NOTE  ##################################
#   This script gets the logging directory (relative to the DB data dir)
#       $ sudo -u postgres scripts/get_database_logging_dir.sh 10000 kushagrasingh
###############################################################################

##############################  Configurations  ##############################

DATABASE_PORT=$1
PG_USERNAME=$2

###############################################################################

echo "SELECT setting FROM pg_settings WHERE name = 'log_directory';" | psql -p ${DATABASE_PORT} postgres --username ${PG_USERNAME}
