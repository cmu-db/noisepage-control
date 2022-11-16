import os
import json
import requests
import shutil
import uuid
from datetime import datetime
from io import StringIO
import random

import tarfile

def create_workload_archive(resource_dir, log_dir, database_id, num_chunks):

    # Get log files (.csv) from logging dir
    log_files = list(filter(lambda x: x.endswith(".csv"), os.listdir(log_dir)))
    log_files.sort(reverse = True)

    # Process only num_chunks files except from the last (that is the current log file, it is not complete)
    files_to_process = log_files[1:num_chunks + 1]

    # Process files and create archive
    archive_path = resource_dir / (database_id + ".tar.gz")
    tar = tarfile.open(archive_path, 'w:gz')
    meta_data = []
    for file_name in files_to_process:
        with open(log_dir / file_name, 'r') as fp:
            queries = fp.readlines()
            num_queries = len(queries)
            sample = random.choices(queries, k = 5)

            meta_data.append({
                'file_name': file_name,
                'num_queries': num_queries,
                'sample': sample
            })

        # Add file to archive
        tar.add(log_dir / file_name)

    tar.close()

    print("Created archive %s" % (archive_path))

    return meta_data, archive_path

def create_state_archive(resource_dir, identifier, state_dir):

    shutil.make_archive(
        resource_dir / identifier, "gztar", resource_dir, identifier
    )
    archive_path = str(resource_dir / identifier) + ".tar.gz"
    print("Created archive %s" % (archive_path))

    return archive_path


# Transfer archive to control plane
def transfer_archive(archive_path, database_id, meta_data, callback_url):

    data = {
        "database_id": database_id,
        "meta_data": meta_data,
    }

    with StringIO(json.dumps(data)) as data_file, open(archive_path, "rb") as fp:

        files = [
            ("workload", ("workload.tar.gz", fp, "application/x-gtar")),
            ("data", ("data.json", data_file, "application/json")),
        ]

        requests.post(callback_url, files=files)

# Transfer archive to control plane
def transfer_state_archive(archive_path, database_id, collected_at, callback_url):

    data = {
        "database_id": database_id,
        "collected_at": collected_at,
    }

    with StringIO(json.dumps(data)) as data_file, open(archive_path, "rb") as fp:

        files = [
            ("state", ("state.tar.gz", fp, "application/x-gtar")),
            ("data", ("data.json", data_file, "application/json")),
        ]

        requests.post(callback_url, files=files)
