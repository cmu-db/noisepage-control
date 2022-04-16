import os
import uuid
import shutil
import logging
from io import StringIO
from datetime import datetime

from django.conf import settings

from primary_worker.services.primary_executor.get_logging_dir import get_logging_dir

logger = logging.getLogger("primary_worker")


def create_workload_archive(capture_start_time, capture_end_time):

    # Get logging dir
    log_dir = get_logging_dir()
    logger.info("Logging dir: %s" % (log_dir))

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
    workload_capture_base_dir = settings.WORKLOAD_CAPTURE_DIR
    workload_capture_dir = workload_capture_base_dir / identifier
    os.mkdir(workload_capture_dir)

    # Copy files to workload capture dir
    for file_name in files_to_process:
        src = log_dir / file_name
        dst = workload_capture_dir / file_name
        shutil.copyfile(src, dst)

    logger.info("Copied log files")

    # 7. Make archive
    shutil.make_archive(
        workload_capture_dir, "gztar", workload_capture_base_dir, identifier
    )
    archive_path = str(workload_capture_base_dir / identifier) + ".tar.gz"

    logger.info("Created archive %s" % (archive_path))

    return archive_path
