sudo apt-get update
sudo apt -y install python3-virtualenv

git clone https://github.com/cmu-db/noisepage-control
cd noisepage-control/
git checkout dbregistration
git pull origin dbregistration

cd primary_daemon/

virtualenv venv
source venv/bin/activate
pip install flask

mkdir -p resources
chmod +x scripts/*.sh

nohup sudo venv/bin/flask run -h 0.0.0.0 -p 9000 >/dev/null 2>&1 &
sleep 5
