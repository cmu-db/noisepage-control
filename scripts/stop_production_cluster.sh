#!/bin/bash

PROJECT_DIR=`pwd`
PRIMARY_PORT="10000"
REPLICA_PORT="10001"

PRIMARY_DIR="${PROJECT_DIR}/production_cluster/primary"
pg_ctl stop -D "${PRIMARY_DIR}"
REPLICA_DIR="${PROJECT_DIR}/production_cluster/replica"
pg_ctl stop -D "${REPLICA_DIR}"

rm -rf "${PROJECT_DIR}/production_cluster"