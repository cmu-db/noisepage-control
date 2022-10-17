import json
from flask import Flask, request
from threading import Thread

from tune import tune_database

app = Flask(__name__)

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
    workload_filename = request.files['workload'].filename
    with open(workload_filename, "wb") as wfp:
        wfp.write(workload_tar)
    
    state_tar = request.files['state'].read()
    state_filename = request.files['state'].filename
    with open(state_filename, "wb") as wfp:
        wfp.write(state_tar)

    callback_url = data["callback_url"]

    thread = Thread(
        target=tune_database, 
        args=(callback_url,)
    )
    thread.start()

    return 'OK'