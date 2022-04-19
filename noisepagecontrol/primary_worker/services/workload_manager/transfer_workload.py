import json
import logging
from io import StringIO

import requests
from django.conf import settings

logger = logging.getLogger("primary_worker")


def transfer_workload(archive_path, event_name, resource_id):
    # Transfer archive to control plane

    control_plane_url = settings.CONTROL_PLANE_URL
    control_plane_port = settings.CONTROL_PLANE_PORT
    tuning_id = settings.TUNING_ID

    url = "http://%s:%s/primary_worker_handler/workload_capture_callback/" % (
        control_plane_url,
        control_plane_port,
    )

    data = {
        "tuning_id": tuning_id,
        "event_name": event_name,
        "resource_id": resource_id,
    }

    with StringIO(json.dumps(data)) as data_file, open(archive_path, "rb") as fp:

        files = [
            ("workload", ("workload.tar.gz", fp, "application/x-gtar")),
            ("data", ("data.json", data_file, "application/json")),
        ]

        headers = {"Content-type": "multipart/form-data"}
        requests.post(url, files=files, headers=headers)
