#!/bin/sh

# Start postgres
service postgresql start

# Create user
echo "CREATE USER ${PG_USERNAME} WITH SUPERUSER;" | psql

# Restore schema; /schema.sql should be mounted while execing 
psql postgres -U ${PG_USERNAME} < /data/dump.sql 

# Move to directory
cd /noisepage-pilot/action/generation

# Run tuning engine
python3 engine.py -o searchspace.json -c /data/garbage_config.yaml

# Move generated file to mounted directory
mv searchspace.json /data/