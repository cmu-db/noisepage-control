FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# Install base reqs
RUN apt-get update
RUN apt-get install -y gnupg wget vim git 

# Install PG
RUN echo "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt focal-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y postgresql-14
# We use a conf file that allows local login without password
COPY pg_hba.conf /etc/postgresql/14/main/pg_hba.conf

# Clone generation code
RUN git clone https://github.com/mkpjnx/noisepage-pilot.git
# Make postgres the owner
RUN chown -R postgres noisepage-pilot
# Install repo reqs
RUN apt-get -y install python3-dev python3-pip libpq-dev
RUN pip3 install pglast pandas numpy SQLAlchemy PyYAML plumbum psycopg2

# Clone index selection code
RUN git clone https://github.com/mkpjnx/index_selection_evaluation.git
RUN chown -R postgres index_selection_evaluation
RUN pip3 install pyhdb

# Tuning exec script
COPY tune.sh tune.sh
RUN chmod +x tune.sh

ENTRYPOINT ["./tune.sh"]

# Exec command:
# docker run -v /Users/kushagrasingh/Desktop/CMUDB/noisepage-control/images/Garbage/data:/data -e PG_USERNAME=cmudb -u postgres -it index