#!/bin/bash

##################################  NOTE  ##################################
#   This script spawns a primary and replica postgres instance
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/stop_production_cluster.sh
###############################################################################

##############################  Configurations  ##############################

PRIMARY_PORT="10000"
REPLICA_PORT="10001"
REPLICATION_USERNAME="repl"

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
#       OSX:    /usr/local/bin
POSTGRES_BIN_DIR="/usr/local/bin"

# This specifies where the postgres cluster should reside
#   Ubuntu: /var/lib/postgresql/14
POSTGRES_ROOT="/var/lib/postgresql/14"

###############################################################################






PROJECT_DIR=`pwd`
PRODUCTION_CLUSTER_DIR="${PROJECT_DIR}/production_cluster"

# Dir for primary and replica
PRIMARY_DIR="${PRODUCTION_CLUSTER_DIR}/primary"
REPLICA_DIR="${PRODUCTION_CLUSTER_DIR}/replica"

# Stop primary and replica
${POSTGRES_BIN_DIR}/pg_ctl stop -D "${PRIMARY_DIR}"
${POSTGRES_BIN_DIR}/pg_ctl stop -D "${REPLICA_DIR}"

# Delete production cluster dir
rm -rf "${PRODUCTION_CLUSTER_DIR}"