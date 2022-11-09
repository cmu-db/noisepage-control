import tarfile
import shutil
import os
from pathlib import Path
import docker
import json

import requests

# IMAGE_NAME = "kushagr2/garbage:v2" # Only garbage
IMAGE_NAME = "kushagr2/garbage:v3" # Garbage + Index

def tune_database(tuning_instance_id, db_name, callback_url):

    # Hack to get the workload and state dir. Need to figure this out
    with tarfile.open("workload.tar.gz") as w:
        workload_dir_name = Path(w.getmembers()[0].name)
        workload_filepath = Path(w.getmembers()[1].name)
        w.extractall()

    with tarfile.open("state.tar.gz") as w:
        state_dir_name = Path(w.getmembers()[0].name)
        ddl_dump_filepath = state_dir_name / "ddl_dump.sql"
        data_dump_filepath = state_dir_name / "data_dump.tar"
        w.extractall()

    shutil.rmtree("data", ignore_errors = True) # ignore doesn't exist error
    os.umask(0)
    os.mkdir("data", 0o777)

    shutil.copy(workload_filepath, "data/workload.csv")
    shutil.copy(ddl_dump_filepath, "data/ddl_dump.sql")
    shutil.copy(data_dump_filepath, "data/data_dump.tar")

    # Generate garbage config
    with open("base_configs/garbage_config.yaml", "r") as fp:
        garabage_config = fp.read()
    garabage_config = garabage_config.replace('{{{db_name}}}', db_name)
    with open("data/garbage_config.yaml", "w") as fp:
        fp.write(garabage_config)

    # Generate index selection config
    with open("base_configs/index_config.json", "r") as fp:
        index_config = fp.read()
    index_config = index_config.replace('{{{db_name}}}', db_name)
    with open("data/index_config.json", "w") as fp:
        fp.write(index_config)

    # Execute image
    parent_dir_path = Path(__file__).parent.resolve()
    client = docker.from_env()
    exec_logs = client.containers.run(
        IMAGE_NAME,
        environment = {
            "PG_USERNAME" : "cmudb",
        },
        user = "postgres",
        volumes = {
            str(parent_dir_path / "data"): {
                'bind': '/data', 'mode': 'rw'
                }
            }, 
        detach = False)

    # Clean up
    os.remove("workload.tar.gz")
    shutil.rmtree(workload_dir_name)
    os.remove("state.tar.gz")
    shutil.rmtree(state_dir_name)



    # Dummy data; TODO: Get from container out
    data = {
        "actions": [
            {
                "command": "CREATE INDEX ppp on resource_manager_resource (available);",
                "benefit": 300.0,
                "reboot_required": False
            }, {
                "command": "ALTER SYSTEM SET max_connections TO '20';",
                "benefit": 200.0,
                "reboot_required": True
            }
        ],
        "tuning_instance_id": tuning_instance_id,
        "exec_logs": exec_logs
    }

    headers = {"Content-type": "application/json"}
    requests.post(callback_url, data=json.dumps(data), headers=headers, timeout=3)
