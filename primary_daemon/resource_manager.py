import os
import json
import requests
import shutil
import uuid
from datetime import datetime
from io import StringIO
import random
import csv
import numpy as np

import tarfile

SAMPLE_SIZE = 10

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

        # Preprocess and malke a copy  
        query_times = []
        num_queries = 0
        sample = []

        with open(log_dir / file_name, 'r') as infile, open(file_name, 'w') as outfile:
            
            queries = csv.reader(infile)
            writer = csv.writer(outfile)
            

            for query in queries:
                # Not a log, continue
                if query[11] != "LOG":
                    continue

                # Duration, push the value to collected times
                if query[13].startswith("duration: "):
                    query_times.append(float(query[13][10:-3]))
                elif query[13].startswith("statement: "): # Write to log file
                    num_queries += 1
                    writer.writerow(query)

                    if len(sample) < SAMPLE_SIZE:
                        sample.append(query[13])

            meta_data.append({
                'file_name': file_name,
                'num_queries': num_queries,
                'sample': sample,
                'p99': np.percentile(query_times, 99),
                'p90': np.percentile(query_times, 90),
                'p75': np.percentile(query_times, 75),
                'p50': np.percentile(query_times, 50),
            })

            # Add file to archive
            tar.add(file_name, arcname = file_name)
            # Delete the temp file
            os.remove(file_name)

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
