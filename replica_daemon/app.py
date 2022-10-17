from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello this is replica worker'

@app.route('/healthcheck/')
def healthcheck():
    return 'OK'

@app.route('/tune/', methods = ['POST'])
def tune():

    data = request.get_json()

    db_name = data["db_name"]
    resource_id = data["resource_id"]
    time_period = data["time_period"]
    callback_url = data["callback_url"]

    print ("Starting thread with", data)

    thread = Thread(
        target=capture_and_transfer_workload, 
        args=(db_name, resource_id, int(time_period), callback_url)
    )
    thread.start()

    return 'OK'