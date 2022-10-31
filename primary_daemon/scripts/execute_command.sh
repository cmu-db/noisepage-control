#!/bin/bash

##################################  NOTE  ##################################
#   This script executes a command
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/execute_command.sh "CREATE INDEX ..." "{{data_dir}}" 1 10000 postgres noisepage_control
###############################################################################

##############################  Configurations  ##############################

CMD=$1
DATA_DIR=$2
REBOOT_REQUIRED=$3
DATABASE_PORT=$4
PG_USERNAME=$5
DATABASE_NAME=$6

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

###############################################################################

# Update config
sudo -u postgres bash -c "echo \"${CMD}\" | psql -p ${DATABASE_PORT} --username ${PG_USERNAME} -d ${DATABASE_NAME}"

# Reboot if required
if [ ${REBOOT_REQUIRED} -eq 1 ]; then
    sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl restart -D '${DATA_DIR}'"
fi
