#!/bin/bash

PROJECT_DIR=`pwd`
PRIMARY_PORT="10000"
REPLICA_PORT="10001"

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin/
#       OSX:    /usr/local/bin/
POSTGRES_BIN_DIR="/usr/local/bin"

# This specifies where the postgres cluster should reside
#   Ubuntu: /var/lib/postgresql/14
PRODUCTION_CLUSTER_DIR="${PROJECT_DIR}/production_cluster"
PRIMARY_DIR="${PRODUCTION_CLUSTER_DIR}/primary"
REPLICA_DIR="${PRODUCTION_CLUSTER_DIR}/replica"

${POSTGRES_BIN_DIR}/pg_ctl stop -D "${PRIMARY_DIR}"
${POSTGRES_BIN_DIR}/pg_ctl stop -D "${REPLICA_DIR}"

rm -rf "${PROJECT_DIR}/production_cluster"