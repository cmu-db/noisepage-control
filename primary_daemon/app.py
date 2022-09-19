from flask import Flask, request

from pathlib import Path

app = Flask(__name__)

from threading import Thread

from primary_executor import PrimaryExecutor
from resource_manager import create_workload_archive, transfer_archive

ROOT_DIR = Path(app.root_path)
SCRIPTS_DIR = ROOT_DIR / "scripts"
RESOURCE_DIR = ROOT_DIR / "resources"

# TODO: Load postgres user from config
database_executor = PrimaryExecutor(SCRIPTS_DIR, "postgres", "10000")

@app.route('/')
def index():
    return 'Hello this is primary worker'

@app.route('/healthcheck/')
def healthcheck():
    return 'OK'

@app.route('/collect_workload/', methods = ['POST'])
def collect_workload():

    data = request.get_json()
    resource_id = data["resource_id"]
    time_period = data["time_period"]
    callback_url = data["callback_url"]

    print ("Starting thread with", data)

    thread = Thread(
        target=capture_and_transfer_workload, 
        args=(resource_id, int(time_period), callback_url)
    )
    thread.start()

    return 'OK'


def capture_and_transfer_workload(resource_id, time_period, callback_url):
    log_dir, start_time, end_time = database_executor.capture_workload(time_period)
    archive_path = create_workload_archive(start_time, end_time, RESOURCE_DIR, log_dir)
    transfer_archive(archive_path, resource_id, callback_url)
