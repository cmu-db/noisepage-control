import tarfile
import shutil
import os
from pathlib import Path
import docker

def tune_database(callback_url, db_name):

    # Hack to get the workload and state dir. Need to figure this out
    with tarfile.open("workload.tar.gz") as w:
        workload_filepath = Path(w.getmembers()[1].name)
        w.extractall()

    with tarfile.open("state.tar.gz") as w:
        pgdump_filepath = Path(w.getmembers()[0].name) / "dump.sql"
        w.extractall()

    shutil.rmtree("data", ignore_errors = True) # ignore doesn't exist error
    os.umask(0)
    os.mkdir("data", 0o777)

    shutil.copy(workload_filepath, "data/workload.csv")
    shutil.copy(pgdump_filepath, "data/schema.sql")

    with open("base_configs/garbage_config.yaml", "r") as fp:
        garabage_config = fp.read()
    garabage_config = garabage_config.replace('{{{db_name}}}', db_name)
    with open("data/garbage_config.yaml", "w") as fp:
        fp.write(garabage_config)

    parent_dir_path = Path(__file__).parent.resolve()

    client = docker.from_env()
    exec_logs = client.containers.run(
        "kushagr2/garbage:v2",
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

    print (exec_logs)
