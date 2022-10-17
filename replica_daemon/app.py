import json
from flask import Flask, request
from threading import Thread

from tune import tune_database

app = Flask(__name__)

# tune_database("", "noisepage_control")

@app.route('/')
def index():
    return 'Hello this is replica worker'

@app.route('/healthcheck/')
def healthcheck():
    return 'OK'

@app.route('/tune/', methods = ['POST'])
def tune():

    data = json.loads(request.files["data"].read().decode("utf-8"))
    
    workload_tar = request.files['workload'].read()
    with open("workload.tar.gz", "wb") as wfp:
        wfp.write(workload_tar)
    
    state_tar = request.files['state'].read()
    with open("state.tar.gz", "wb") as wfp:
        wfp.write(state_tar)

    callback_url = data["callback_url"]
    db_name = data["db_name"]

    thread = Thread(
        target=tune_database, 
        args=(callback_url, db_name)
    )
    thread.start()

    return 'OK'
