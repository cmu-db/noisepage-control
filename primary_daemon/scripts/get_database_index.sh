#!/bin/bash

##################################  NOTE  ##################################
#   This script gets the catalog for a datbase
#       Credits -- https://dba.stackexchange.com/a/295622
#       $ sudo -u postgres scripts/get_database_catalog.sh \
#                          10000 cmudb noisepage_control
###############################################################################

##############################  Configurations  ##############################

DATABASE_PORT=$1
PG_USERNAME=$2
DATABASE_NAME=$3

###############################################################################

sudo -u postgres bash -c "echo \"SELECT n.nspname AS schema
     , i.indrelid::regclass::text AS table
     , c.relname AS index
     , a.amname AS index_method
     , opc.operator_classes
     , pg_get_indexdef(i.indexrelid) AS index_definition
FROM   pg_catalog.pg_namespace n
JOIN   pg_catalog.pg_class     c ON c.relnamespace = n.oid
JOIN   pg_catalog.pg_index     i ON i.indexrelid = c.oid
JOIN   pg_catalog.pg_am        a ON a.oid = c.relam
CROSS  JOIN LATERAL (
   SELECT ARRAY (SELECT opc.opcname
                 FROM   unnest(i.indclass::oid[]) WITH ORDINALITY o(oid, ord)
                 JOIN   pg_opclass opc ON opc.oid = o.oid
                 ORDER  BY o.ord)
   ) opc(operator_classes)
WHERE  n.nspname !~ '^pg_'
AND    c.relkind = 'i'
ORDER  BY 1, 2, 3, 4;\" | psql -p ${DATABASE_PORT} --username ${PG_USERNAME} -d ${DATABASE_NAME}"