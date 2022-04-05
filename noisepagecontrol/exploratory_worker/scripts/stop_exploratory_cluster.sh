#!/bin/bash

##################################  NOTE  ##################################
#   This script tears down the exploratory postgres cluster
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/stop_production_cluster.sh
###############################################################################

##############################  Configurations  ##############################

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
#       OSX:    /usr/local/bin
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

# This specifies where the postgres cluster should reside
#   Ubuntu: /var/lib/postgresql/14
POSTGRES_ROOT="/var/lib/postgresql/14"

###############################################################################

# TODO Tim: pass in CLUSTER_DIR path
CLUSTER_DIR="${POSTGRES_ROOT}/exploratory"

# Stop primary and replica
${POSTGRES_BIN_DIR}/pg_ctl stop -D "${CLUSTER_DIR}"

# Delete production cluster dir
rm -rf "${CLUSTER_DIR}"
