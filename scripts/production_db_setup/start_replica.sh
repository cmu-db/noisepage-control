# sudo sh -c 'echo "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
# wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# sudo apt-get update
# sudo apt-get -y install postgresql-14

#!/bin/bash

##################################  NOTE  ##################################
#   This script spawns a replica postgres instance
###############################################################################

##############################  Configurations  ##############################

PRIMARY_IP="54.242.174.185"
PRIMARY_PORT="10000"
REPLICA_PORT="10001"
REPLICATION_USERNAME="repl"

# This specifies where the postgres cluster should reside
POSTGRES_ROOT="/var/lib/postgresql/14"

# This specifies where the postgres binaries are (initdb, pg_ctl, etc.)
POSTGRES_BIN_DIR="/usr/lib/postgresql/14/bin"

###############################################################################

REPLICA_DIR="${POSTGRES_ROOT}/production_cluster"

# Create fresh dir
sudo -u postgres rm -rf "${REPLICA_DIR}"
sudo -u postgres mkdir -p "${REPLICA_DIR}"

# Create replica
sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_basebackup --pgdata '${REPLICA_DIR}' --format=p --write-recovery-conf --checkpoint=fast --label=mffb --progress --host ${PRIMARY_IP} --port=${PRIMARY_PORT} --username='${REPLICATION_USERNAME}'"
sudo -u postgres bash -c "echo 'port = ${REPLICA_PORT}' >> '${REPLICA_DIR}/postgresql.conf'"
sudo -u postgres bash -c "echo \"primary_conninfo = 'user=${REPLICATION_USERNAME} port=${PRIMARY_PORT} host=${PRIMARY_IP} application_name=db02.repl'\" >> '${REPLICA_DIR}/postgresql.conf'"

# Fix permissions
sudo -u postgres chmod -R 750 "${REPLICA_DIR}"

# Start replica
sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl -D "${REPLICA_DIR}" -l "${REPLICA_DIR}/logfile" start"

# sudo -u postgres bash -c "${POSTGRES_BIN_DIR}/pg_ctl -D "${REPLICA_DIR}" stop"
