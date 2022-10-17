from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello this is replica worker'

@app.route('/healthcheck/')
def healthcheck():
    return 'OK'

@app.route('/tune/', methods = ['POST'])
def tune():

    data = json.loads(request.FILES["data"].read().decode("utf-8"))
    workload_tar = request.files['workload.tar.gz'].read()
    state_tar = request.files['state.tar.gz'].read()

    print (data)
    print (workload_tar)
    print (state_tar)

    return 'OK'