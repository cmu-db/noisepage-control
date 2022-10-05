#!/bin/bash

##################################  NOTE  ##################################
#   This script gets pg_dump for a database
###############################################################################

##############################  Configurations  ##############################

DATABASE_PORT=$1
PG_USERNAME=$2
DATABASE_NAME=$3

###############################################################################

sudo -u postgres bash -c "pg_dump -s -p ${DATABASE_PORT} --username ${PG_USERNAME} -d ${DATABASE_NAME}"
