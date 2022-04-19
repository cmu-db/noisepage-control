import logging
import time
from datetime import datetime
from threading import Lock

from primary_worker.services.primary_executor.disable_logging import (
    disable_logging,
)
from primary_worker.services.primary_executor.enable_logging import (
    enable_logging,
)

from .create_workload_archive import create_workload_archive
from .transfer_workload import transfer_workload

logger = logging.getLogger("primary_worker")

"""
    Lock to prevent multiple concurrent workload captures
"""
WORKLOAD_CAPTURE_MUTEX = Lock()


def capture_workload(time_period, command_name, resource_id):
    """
    This method captures the workload on a primary instance.
    Only allow one concurrent capture;
    synchronised via `WORKLOAD_CAPTURE_MUTEX`
    """

    logger.info("Waiting for mutex")
    WORKLOAD_CAPTURE_MUTEX.acquire()
    logger.info("Starting workload capture for %d seconds" % (time_period))

    try:
        # Enable logging
        enable_logging()
        logger.info("Enabled logging")

        # Wait for time_period seconds
        capture_start_time = datetime.now()
        for it in range(0, time_period, 5):
            time.sleep(5)
            logger.info("Captured %d seconds" % (it + 5))
        capture_end_time = datetime.now()

        # Disable logging
        disable_logging()
        logger.info("Disabled logging")

        # Create workload archive
        archive_path = create_workload_archive(capture_start_time, capture_end_time)

        # Transfer archive to control plane
        transfer_workload(archive_path, command_name, resource_id)

    finally:
        WORKLOAD_CAPTURE_MUTEX.release()
