#!/bin/bash

##################################  NOTE  ##################################
#   This script stops logging for a database instance
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/stop_database_logging.sh "/Users/kushagrasingh/Desktop/CMU DB/noisepage-control/production_cluster/primary" 10000
###############################################################################

##############################  Configurations  ##############################

DATA_DIR=$1
DATABASE_PORT=$2
PG_USERNAME=$3

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
#       OSX:    /usr/local/bin
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

###############################################################################


echo "ALTER SYSTEM SET log_destination='stderr';" | psql -p ${DATABASE_PORT} postgres --username "${PG_USERNAME}"
echo "ALTER SYSTEM SET log_statement='none';" | psql -p ${DATABASE_PORT} postgres --username "${PG_USERNAME}"
echo "ALTER SYSTEM SET logging_collector=off;" | psql -p ${DATABASE_PORT} postgres --username "${PG_USERNAME}"


${POSTGRES_BIN_DIR}/pg_ctl restart -D "${DATA_DIR}"
