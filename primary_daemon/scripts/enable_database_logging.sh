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
LOG_ROTATION_AGE=$4

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

###############################################################################

# Update config
sudo -u postgres bash -c "echo \"ALTER SYSTEM SET log_rotation_age=${LOG_ROTATION_AGE};\" | psql -p ${DATABASE_PORT}"
sudo -u postgres bash -c "echo \"ALTER SYSTEM SET log_destination='csvlog';\" | psql -p ${DATABASE_PORT}"
sudo -u postgres bash -c "echo \"ALTER SYSTEM SET log_statement='all';\" | psql -p ${DATABASE_PORT}"
sudo -u postgres bash -c "echo \"ALTER SYSTEM SET logging_collector=on;\" | psql -p ${DATABASE_PORT}"

# Restart postgres
sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl restart -D '${DATA_DIR}'"
