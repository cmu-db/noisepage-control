# noisepage-control
NoisePage Autonomous Control Plane Infrastructure


## Set up server


1. Install RabbitMQ
```
# Ubuntu:
sudo apt-get install wget apt-transport-https -y
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
echo "deb https://dl.bintray.com/rabbitmq-erlang/debian focal erlang-22.x" | sudo tee /etc/apt/sources.list.d/rabbitmq.list
sudo apt-get install rabbitmq-server -y --fix-missing
sudo systemctl status rabbitmq-server

# macOS:
brew install rabbitmq
brew services restart rabbitmq
```
2. Install Postgres and setup DB

```
# Ubuntu:
sudo apt install postgresql postgresql-contrib
sudo -u postgres -i
psql
    CREATE USER cmudb WITH superuser ENCRYPTED PASSWORD 'cmudb@2021';
    CREATE DATABASE noisepage_control WITH OWNER cmudb ENCODING 'UTF8';

# macOS
brew install postgresql
brew services restart postgresql@14
psql
    CREATE USER cmudb WITH superuser ENCRYPTED PASSWORD 'cmudb@2021';
    CREATE DATABASE noisepage_control WITH OWNER cmudb ENCODING 'UTF8';
```

3. Install required packages

```
pip install -r requirements.txt
```

4. Migrate (apply postgres table schemas)
```
python control_plane/manage.py migrate
```

4. Run the server
```
python control_plane/manage.py runserver
```

## Set up frontend
1. Install nvm, npm LTS, yarn
```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
nvm install --lts
npm install --global yarn
```
2. Install node modules
```
cd control_plane/client-app
yarn install
```
3. Start frontend
```
yarn start
```
