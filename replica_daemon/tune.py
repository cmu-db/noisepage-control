import tarfile
import shutil
import os
from pathlib import Path
import docker
import json
import glob
import requests

# IMAGE_NAME = "kushagr2/garbage:v2" # Only garbage
IMAGE_NAME = "kushagr2/garbage:v4" # Garbage + Index

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

    # Parse generated file for actions
    results_dir_path = parent_dir_path / "data" /  "benchmark_results/"

    actions = []
    for file in os.listdir(results_dir_path):
        if not file.endswith(".sql"): # Ignore non SQL files
            continue

        with open(results_dir_path / file, "r") as fp:
            for action in fp.readlines():
                actions.append({
                    "command": action.strip("\n"),
                    "benefit": 100.0,
                    "reboot_required": False if action.startswith("create index") else True,
                })


    # Clean up
    os.remove("workload.tar.gz")
    shutil.rmtree(workload_dir_name)
    os.remove("state.tar.gz")
    shutil.rmtree(state_dir_name)
    shutil.rmtree("data")

    data = {
        "actions": actions,
        "tuning_instance_id": tuning_instance_id,
        "exec_logs": exec_logs
    }

    headers = {"Content-type": "application/json"}
    requests.post(callback_url, data=json.dumps(data), headers=headers, timeout=3)
