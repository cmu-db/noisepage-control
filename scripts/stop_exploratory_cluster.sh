#!/bin/bash

##################################  NOTE  ##################################
#   This script tears down the exploratory postgres cluster
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/stop_exploratory_cluster.sh CLUSTER_DIR
###############################################################################

CLUSTER_DIR=$1

if [[ -z $CLUSTER_DIR ]]
then
    echo "Missing CLUSTER_DIR. Command: sudo -u postgres scripts/stop_exploratory_cluster.sh CLUSTER_DIR"
    exit
fi

##############################  Configurations  ##############################

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
#       OSX:    /usr/local/bin
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

###############################################################################

# Stop primary and replica
${POSTGRES_BIN_DIR}/pg_ctl stop -D "${CLUSTER_DIR}"

# Delete production cluster dir
rm -rf "${CLUSTER_DIR}"
