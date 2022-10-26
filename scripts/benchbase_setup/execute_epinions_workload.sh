#!/bin/bash

# TODO: Please manually update your connection string in benchbase/target/benchbase-postgres/config/postgres/sample_epinions_config.xml
cd ~/benchbase/target/benchbase-postgres
java -jar benchbase.jar -b epinions -c config/postgres/sample_epinions_config.xml --execute=true
