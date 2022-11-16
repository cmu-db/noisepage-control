import os
import uuid
import json
import tarfile
import datetime

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
database_executor.enable_logging()

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
    database_id = data["database_id"]
    callback_url = data["callback_url"]

    print ("Starting thread with", data)

    thread = Thread(
        target=capture_and_transfer_state, 
        args=(db_name, database_id, callback_url)
    )
    thread.start()

    return 'OK'

def capture_and_transfer_state(database_name, database_id, callback_url):

    archive_path = RESOURCE_DIR / (database_id + "_state.tar.gz")
    tar = tarfile.open(archive_path, 'w:gz')

    collected_at = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Write current catalog
    catalog = database_executor.get_database_catalog(database_name)
    with open(RESOURCE_DIR / "catalog.txt", "w") as fp:
        fp.write(catalog)
    tar.add(RESOURCE_DIR / "catalog.txt", arcname = "catalog.txt")

    # Write current indexes
    index_info = database_executor.get_database_index(database_name)
    with open(RESOURCE_DIR / "index.txt", "w") as fp:
        fp.write(index_info)
    tar.add(RESOURCE_DIR / "index.txt", arcname = "index.txt")

    # Write ddl dump
    ddl_dump = database_executor.get_database_ddl_dump(database_name)
    with open(RESOURCE_DIR / "ddl_dump.sql", "w") as fp:
        fp.write(ddl_dump)
    tar.add(RESOURCE_DIR / "ddl_dump.sql", arcname = "ddl_dump.sql")

    # Write ddl dump
    dump_tar = database_executor.get_database_data_dump_tar(database_name)
    with open(RESOURCE_DIR / "data_dump.tar", "wb") as fp:
        fp.write(dump_tar)
    tar.add(RESOURCE_DIR / "data_dump.tar", arcname = "data_dump.tar")
    tar.close()

    transfer_state_archive(archive_path, database_id, collected_at, callback_url)

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
