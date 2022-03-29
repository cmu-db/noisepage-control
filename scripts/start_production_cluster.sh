#!/bin/bash

# This script spawns a primary and replica postgres instance
# It should be executed from project root

PRIMARY_PORT="10000"
REPLICA_PORT="10001"
REPLICATION_USERNAME="repl"

PROJECT_DIR=`pwd`
PRODUCTION_CLUSTER_DIR="${PROJECT_DIR}/production_cluster"
PRIMARY_DIR="${PRODUCTION_CLUSTER_DIR}/primary"
REPLICA_DIR="${PRODUCTION_CLUSTER_DIR}/replica"

# Stop running instances if up
"${PROJECT_DIR}/scripts/stop_production_cluster.sh"

# Create fresh dir
rm -rf "${PRODUCTION_CLUSTER_DIR}"
mkdir "${PRODUCTION_CLUSTER_DIR}"

# Init primary
initdb "${PRIMARY_DIR}"
echo "port = ${PRIMARY_PORT}" >> "${PRIMARY_DIR}/postgresql.conf"
echo "wal_level = replica" >> "${PRIMARY_DIR}/postgresql.conf"
echo "wal_compression = on" >> "${PRIMARY_DIR}/postgresql.conf"
echo "max_wal_senders = 10" >> "${PRIMARY_DIR}/postgresql.conf"
echo "wal_keep_size = '1GB'" >> "${PRIMARY_DIR}/postgresql.conf"

# Start primary
pg_ctl -D "${PRIMARY_DIR}" -l "${PRIMARY_DIR}/logfile" start

# Create replication user
createuser -p ${PRIMARY_PORT} --replication "${REPLICATION_USERNAME}"

# Create replication slot
echo "select * from pg_create_physical_replication_slot('db02_repl_slot');" \
    | psql -p 10000 template1





# Create replica
mkdir "${REPLICA_DIR}"
pg_basebackup --pgdata "${REPLICA_DIR}" \
    --format=p --write-recovery-conf --checkpoint=fast \
    --label=mffb --progress --port=${PRIMARY_PORT} \
    --username="${REPLICATION_USERNAME}"

echo "port = ${REPLICA_PORT}" >> "${REPLICA_DIR}/postgresql.conf"
echo "primary_conninfo = 'user=${REPLICATION_USERNAME} port=${PRIMARY_PORT} host=localhost application_name=db02.repl'" >> "${REPLICA_DIR}/postgresql.conf"

# Update permissions
chmod -R 750 "${REPLICA_DIR}"

# Start replica server
pg_ctl -D "${REPLICA_DIR}" -l "${REPLICA_DIR}/logfile" start
