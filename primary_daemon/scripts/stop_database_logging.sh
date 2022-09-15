#!/bin/bash

##################################  NOTE  ##################################
#   This script stops logging for a database instance
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/start_database_logging.sh "{{data_dir}}" 10000 postgres
###############################################################################

##############################  Configurations  ##############################

DATA_DIR=$1
DATABASE_PORT=$2
PG_USERNAME=$3

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

###############################################################################

# Update config
sudo -u postgres bash -c "echo \"ALTER SYSTEM SET log_destination='stderr';\" | psql -p ${DATABASE_PORT}"
sudo -u postgres bash -c "echo \"ALTER SYSTEM SET log_statement='none';\" | psql -p ${DATABASE_PORT}"
sudo -u postgres bash -c "echo \"ALTER SYSTEM SET logging_collector=off;\" | psql -p ${DATABASE_PORT}"


# Restart postgres
sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl restart -D '${DATA_DIR}'"
