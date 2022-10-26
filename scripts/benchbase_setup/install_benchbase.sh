#!/bin/bash

sudo apt update
sudo apt install -y openjdk-17-jdk

# Clone and build BenchBase using the postgres profile
cd ~
if [ ! -d "benchbase" ]; then
    git clone --depth 1 https://github.com/timlee0119/benchbase.git
fi
cd benchbase
./mvnw clean package -DskipTests -P postgres

# This produces artifacts in the target folder, which can be extracted
cd target
tar xvzf benchbase-postgres.tgz
