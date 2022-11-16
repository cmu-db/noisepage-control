import os
import uuid
import json

from flask import Flask, request
import requests

from pathlib import Path

app = Flask(__name__)

from threading import Thread

from primary_executor import PrimaryExecutor
from resource_manager import create_workload_archive, transfer_archive, create_state_archive, transfer_state_archive

ROOT_DIR = Path(app.root_path)
SCRIPTS_DIR = ROOT_DIR / "scripts"
RESOURCE_DIR = ROOT_DIR / "resources"

# TODO: Load postgres user from config
database_executor = PrimaryExecutor(SCRIPTS_DIR, "postgres", "10000")

print (database_executor.get_database_catalog("postgres"))
print (database_executor.get_database_index("postgres"))

@app.route('/')
def index():
    return 'Hello this is primary worker'

@app.route('/healthcheck/')
def healthcheck():
    return 'OK'

@app.route('/collect_workload/', methods = ['POST'])
def collect_workload():

    data = request.get_json()
    database_id = data["database_id"]
    callback_url = data["callback_url"]
    num_chunks = data["num_chunks"] # Previously completed chunks

    print ("Starting thread with", data)

    thread = Thread(
        target=capture_and_transfer_workload, 
        args=(database_id, callback_url, int(num_chunks))
    )
    thread.start()

    return 'OK'

@app.route('/apply/', methods = ['POST'])
def apply():

    data = request.get_json()

    data = request.get_json()
    db_name = data["db_name"]
    command = data["command"]
    reboot_required = data["reboot_required"]
    action_id = data["action_id"]
    callback_url = data["callback_url"]

    print ("Starting thread with", data)

    thread = Thread(
        target=apply_action, 
        args=(db_name, command, reboot_required, action_id, callback_url)
    )
    thread.start()

    return 'OK'


def capture_and_transfer_workload(database_id, callback_url, num_chunks):
    log_dir = database_executor.get_logging_dir()
    meta_data, archive_path = create_workload_archive(RESOURCE_DIR, log_dir, database_id, num_chunks)
    transfer_archive(archive_path, database_id, meta_data, callback_url)


@app.route('/collect_state/', methods = ['POST'])
def collect_state():

    data = request.get_json()
    db_name = data["db_name"]
    resource_id = data["resource_id"]
    callback_url = data["callback_url"]

    print ("Starting thread with", data)

    thread = Thread(
        target=capture_and_transfer_state, 
        args=(db_name, resource_id, callback_url)
    )
    thread.start()

    return 'OK'

def capture_and_transfer_state(database_name, resource_id, callback_url):

    # Create a new dir for collected states
    identifier = str(uuid.uuid4())
    state_dir = RESOURCE_DIR / identifier
    os.mkdir(state_dir)


    # Write current catalog
    catalog = database_executor.get_database_catalog(database_name)
    with open(state_dir / "catalog.txt", "w") as fp:
        fp.write(catalog)

    # Write current indexes
    index_info = database_executor.get_database_index(database_name)
    with open(state_dir / "index.txt", "w") as fp:
        fp.write(index_info)

    # Write ddl dump
    ddl_dump = database_executor.get_database_ddl_dump(database_name)
    with open(state_dir / "ddl_dump.sql", "w") as fp:
        fp.write(ddl_dump)

    # Write ddl dump
    dump_tar = database_executor.get_database_data_dump_tar(database_name)
    with open(state_dir / "data_dump.tar", "wb") as fp:
        fp.write(dump_tar)

    archive_path = create_state_archive(RESOURCE_DIR, identifier, state_dir)
    transfer_state_archive(archive_path, resource_id, callback_url)


def apply_action(database_name, command, reboot_required, action_id, callback_url):

    # Execute on primary
    database_executor.apply_action(command, reboot_required, database_name)

    # Hit callback
    # TODO: Add failure status?
    data = {
        "action_id": action_id,
    }        
    headers = {"Content-type": "application/json"}
    requests.post(callback_url, data=json.dumps(data), headers=headers, timeout=3)
