# Install pre reqs
sudo apt-get update
sudo apt-get -y install python3-virtualenv ca-certificates curl gnupg lsb-release

# Install and start docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo service docker start

# Clone daemon code
sudo rm -rf noisepage-control
git clone https://github.com/cmu-db/noisepage-control
cd noisepage-control/
git checkout dbregistration
git pull origin dbregistration
cd replica_daemon/
chmod +x scripts/*.sh

# Install daemon reqs
virtualenv venv
source venv/bin/activate
pip install flask requests docker

# Kill the running replica daemon
if sudo lsof -t -i:9000 > /dev/null; then
    sudo kill $(sudo lsof -t -i:9000)
fi
# Start replica daemon
sudo kill $(sudo lsof -t -i:9000)
nohup sudo venv/bin/flask run -h 0.0.0.0 -p 9000 > ~/.replica_daemon.log 2>&1 &
sleep 5
