#!/bin/bash
set -e

##################################  NOTE  ##################################
#   This script spawns a exploratory Postgres cluster that optionally takes a snapshot
#   from the production replica cluster.
#
#   Script should be run as postgres user;
#       $ sudo -u postgres scripts/start_exploratory_cluster.sh PORT [-s]
###############################################################################

PORT=$1

if [[ -z $PORT ]]
then
    echo "Missing PORT. Command: sudo -u postgres scripts/start_exploratory_cluster.sh PORT [-s]"
    exit
fi

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

EXP_CLUSTER_DIR="$POSTGRES_ROOT/exploratory_$PORT"  # TODO: parameterize

# Create fresh dir
rm -rf "$EXP_CLUSTER_DIR"
mkdir -p "$EXP_CLUSTER_DIR"

# Init exploratory cluster
$POSTGRES_BIN_DIR/initdb "$EXP_CLUSTER_DIR"
echo "port = $PORT" >> "$EXP_CLUSTER_DIR/postgresql.conf"

if [[ $2 == "-s" ]]; then
    # Copy subdirectories in replica's PG_DATA to exploratory's PG_DATA
    REPLICA_CLUSTER_DIR="$POSTGRES_ROOT/main"  # TODO: parameterize
    find $REPLICA_CLUSTER_DIR -mindepth 1 -maxdepth 1 -type d -exec cp -r {} $EXP_CLUSTER_DIR \;
fi

# Start exploratory cluster
$POSTGRES_BIN_DIR/pg_ctl -D "$EXP_CLUSTER_DIR" -l "$EXP_CLUSTER_DIR/logfile" start
