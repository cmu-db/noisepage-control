sudo apt-get update
sudo apt -y install python3-virtualenv

git clone https://github.com/cmu-db/noisepage-control
cd noisepage-control/
git checkout dbregistration
git pull origin dbregistration

cd replica_daemon/

virtualenv venv
source venv/bin/activate
pip install flask
pip install requests

chmod +x scripts/*.sh

nohup sudo venv/bin/flask run -h 0.0.0.0 -p 9000 > ~/.replica_daemon.log 2>&1 &
sleep 5
