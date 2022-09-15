#!/bin/bash

##################################  NOTE  ##################################
#   This script gets the database data directory
#       $ sudo -u postgres scripts/get_database_data_dir.sh 10000 kushagrasingh
###############################################################################

##############################  Configurations  ##############################

DATABASE_PORT=$1
PG_USERNAME=$2

###############################################################################

sudo -u postgres bash -c "echo \"SELECT setting FROM pg_settings WHERE name = 'data_directory';\" | psql -p ${DATABASE_PORT} --username ${PG_USERNAME}"