#!/bin/bash

##################################  NOTE  ##################################
#   This script spawns a primary postgres instance
###############################################################################

##############################  Configurations  ##############################

PRIMARY_IP="18.217.99.54"
PRIMARY_PORT="10000"
REPLICA_IP="18.222.240.209"
REPLICATION_USERNAME="repl"

# This specifies where the postgres cluster should reside
POSTGRES_ROOT="/var/lib/postgresql/14"

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

###############################################################################

PRIMARY_DIR="${POSTGRES_ROOT}/production_cluster"

# Create fresh dir
sudo -u postgres rm -rf "${PRIMARY_DIR}"
sudo -u postgres mkdir -p "${PRIMARY_DIR}"

# Init primary
sudo -u postgres ${POSTGRES_BIN_DIR}/initdb "${PRIMARY_DIR}"
sudo -u postgres bash -c "echo 'port = ${PRIMARY_PORT}' >> '${PRIMARY_DIR}/postgresql.conf'"
sudo -u postgres bash -c "echo 'wal_level = replica' >> '${PRIMARY_DIR}/postgresql.conf'"
sudo -u postgres bash -c "echo 'wal_compression = on' >> '${PRIMARY_DIR}/postgresql.conf'"
sudo -u postgres bash -c "echo 'max_wal_senders = 10' >> '${PRIMARY_DIR}/postgresql.conf'"
sudo -u postgres bash -c "echo 'wal_keep_size = 1GB' >> '${PRIMARY_DIR}/postgresql.conf'"
sudo -u postgres bash -c "echo \"listen_addresses = '*'\" >> '${PRIMARY_DIR}/postgresql.conf'"

# Allow replica to access
sudo -u postgres bash -c "echo \"host    replication     ${REPLICATION_USERNAME}    ${REPLICA_IP}/32       trust\" >> '${PRIMARY_DIR}/pg_hba.conf'"

# Start primary
sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl -D '${PRIMARY_DIR}' -l '${PRIMARY_DIR}/logfile' start"
sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl -D '${PRIMARY_DIR}' restart"

# Create replication user
sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/createuser -p ${PRIMARY_PORT} --replication '${REPLICATION_USERNAME}'"

# Create replication slot
REPLICATION_SLOT_COMMAND="select * from pg_create_physical_replication_slot('db02_repl_slot');"
sudo -u postgres bash -c "echo \"${REPLICATION_SLOT_COMMAND}\" | psql -p ${PRIMARY_PORT} template1"

# sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl -D '${PRIMARY_DIR}' stop"
