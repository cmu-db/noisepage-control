#!/bin/bash

##################################  NOTE  ##################################
#   This script gets complete pg_dump in a tar form for a database
###############################################################################

##############################  Configurations  ##############################

DATABASE_PORT=$1
PG_USERNAME=$2
DATABASE_NAME=$3

###############################################################################

sudo -u postgres bash -c "pg_dump -p ${DATABASE_PORT} --username ${PG_USERNAME} -F t ${DATABASE_NAME}"
