import os
import shutil
import uuid
from datetime import datetime

def create_workload_archive(capture_start_time, capture_end_time, resource_dir, log_dir):

    # Get log files (.csv) from logging dir
    log_files = set(filter(lambda x: x.endswith(".csv"), os.listdir(log_dir)))

    # Process only files where last modification time > capture start time
    files_to_process = []
    for file_name in log_files:
        complete_file_path = log_dir / file_name
        last_modification_time = datetime.fromtimestamp(
            os.path.getmtime(complete_file_path)
        )
        if last_modification_time > capture_start_time:
            files_to_process.append(file_name)

    # Create new directory for current capture
    identifier = str(uuid.uuid4())
    workload_capture_base_dir = resource_dir
    workload_capture_dir = workload_capture_base_dir / identifier
    os.mkdir(workload_capture_dir)

    # Copy files to workload capture dir
    for file_name in files_to_process:
        src = log_dir / file_name
        dst = workload_capture_dir / file_name
        shutil.copyfile(src, dst)

    print("Copied log files")

    # 7. Make archive
    shutil.make_archive(
        workload_capture_dir, "gztar", workload_capture_base_dir, identifier
    )
    archive_path = str(workload_capture_base_dir / identifier) + ".tar.gz"

    print("Created archive %s" % (archive_path))

    return archive_path


# Transfer archive to control plane
def transfer_archive(archive_path, resource_id, callback_url):

    data = {
        "resource_id": resource_id,
    }

    with StringIO(json.dumps(data)) as data_file, open(archive_path, "rb") as fp:

        files = [
            ("workload", ("workload.tar.gz", fp, "application/x-gtar")),
            ("data", ("data.json", data_file, "application/json")),
        ]

        requests.post(callback_url, files=files)
