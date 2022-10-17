#!/bin/bash

##################################  NOTE  ##################################
#   This script gets the catalog for a datbase
#       Credits -- https://dba.stackexchange.com/a/195721
#       $ sudo -u postgres scripts/get_database_catalog.sh \
#                          10000 cmudb noisepage_control
###############################################################################

##############################  Configurations  ##############################

DATABASE_PORT=$1
PG_USERNAME=$2
DATABASE_NAME=$3

###############################################################################

sudo -u postgres bash -c \
    "echo \"SELECT c.oid,
  n.nspname,
  c.relname, t.*
FROM pg_catalog.pg_class c
LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
CROSS JOIN LATERAL (
  SELECT a.attname,
    pg_catalog.format_type(a.atttypid, a.atttypmod),
    (
      SELECT substring(pg_catalog.pg_get_expr(d.adbin, d.adrelid) for 128)
      FROM pg_catalog.pg_attrdef d
      WHERE d.adrelid = a.attrelid
        AND d.adnum = a.attnum
        AND a.atthasdef
    ),
    a.attnotnull, a.attnum,
    (
      SELECT c.collname
      FROM
        pg_catalog.pg_collation c,
        pg_catalog.pg_type t
      WHERE c.oid = a.attcollation
        AND t.oid = a.atttypid
        AND a.attcollation <> t.typcollation
    ) AS attcollation
  FROM pg_catalog.pg_attribute a
  WHERE a.attrelid = c.oid
    AND a.attnum > 0
    AND NOT a.attisdropped
) AS t
WHERE n.nspname ~ '^(public)$'  -- YOUR SCHEMA HERE
AND pg_catalog.pg_table_is_visible(c.oid);\" | psql -p ${DATABASE_PORT} --username ${PG_USERNAME} -d ${DATABASE_NAME}"
