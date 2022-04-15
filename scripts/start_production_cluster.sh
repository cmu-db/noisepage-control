#!/bin/bash

##################################  NOTE  ##################################
#   This script spawns a primary and replica postgres instance
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/start_production_cluster.sh
###############################################################################

##############################  Configurations  ##############################

PRIMARY_PORT="10000"
REPLICA_PORT="10001"
REPLICATION_USERNAME="repl"

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
# Common paths:
#       Ubuntu: /usr/lib/postgresql/14/bin
#       OSX:    /usr/local/bin
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

# This specifies where the postgres cluster should reside
#   Ubuntu: /var/lib/postgresql/14
POSTGRES_ROOT="/var/lib/postgresql/14"

###############################################################################






PROJECT_DIR=`pwd`
PRODUCTION_CLUSTER_DIR="${POSTGRES_ROOT}/production_cluster"

# Stop running instances if up
"${PROJECT_DIR}/scripts/stop_production_cluster.sh"

# Create fresh dir
rm -rf "${PRODUCTION_CLUSTER_DIR}"
mkdir -p "${PRODUCTION_CLUSTER_DIR}"

# Dir for primary and replica
PRIMARY_DIR="${PRODUCTION_CLUSTER_DIR}/primary"
REPLICA_DIR="${PRODUCTION_CLUSTER_DIR}/replica"

# Init primary
${POSTGRES_BIN_DIR}/initdb "${PRIMARY_DIR}"
echo "port = ${PRIMARY_PORT}" >> "${PRIMARY_DIR}/postgresql.conf"
echo "wal_level = replica" >> "${PRIMARY_DIR}/postgresql.conf"
echo "wal_compression = on" >> "${PRIMARY_DIR}/postgresql.conf"
echo "max_wal_senders = 10" >> "${PRIMARY_DIR}/postgresql.conf"
echo "wal_keep_size = '1GB'" >> "${PRIMARY_DIR}/postgresql.conf"

# Start primary
${POSTGRES_BIN_DIR}/pg_ctl -D "${PRIMARY_DIR}" -l "${PRIMARY_DIR}/logfile" start

# Create replication user
${POSTGRES_BIN_DIR}/createuser -p ${PRIMARY_PORT} --replication "${REPLICATION_USERNAME}"

# Create replication slot
echo "select * from pg_create_physical_replication_slot('db02_repl_slot');" \
    | psql -p ${PRIMARY_PORT} template1

# Create replica
mkdir "${REPLICA_DIR}"
${POSTGRES_BIN_DIR}/pg_basebackup --pgdata "${REPLICA_DIR}" \
    --format=p --write-recovery-conf --checkpoint=fast \
    --label=mffb --progress --port=${PRIMARY_PORT} \
    --username="${REPLICATION_USERNAME}"

echo "port = ${REPLICA_PORT}" >> "${REPLICA_DIR}/postgresql.conf"
echo "primary_conninfo = 'user=${REPLICATION_USERNAME} port=${PRIMARY_PORT} host=localhost application_name=db02.repl'" >> "${REPLICA_DIR}/postgresql.conf"

# Update permissions
chmod -R 750 "${REPLICA_DIR}"

# Start replica server
${POSTGRES_BIN_DIR}/pg_ctl -D "${REPLICA_DIR}" -l "${REPLICA_DIR}/logfile" start
