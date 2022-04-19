import json
import logging
from io import StringIO

import requests
from django.conf import settings

logger = logging.getLogger("exploratory_worker")


def transfer_data(command_name, resource_id, archive_path):
    # Transfer archive to control plane

    control_plane_url = settings.CONTROL_PLANE_URL
    control_plane_port = settings.CONTROL_PLANE_PORT
    tuning_id = settings.TUNING_ID

    url = "http://%s:%s/exploratory_worker_handler/data_collector_callback/" % (
        control_plane_url,
        control_plane_port,
    )

    data = {
        "tuning_id": tuning_id,
        "command_name": command_name,
        "resource_id": resource_id,
    }

    with StringIO(json.dumps(data)) as data_file, open(archive_path, "rb") as fp:

        files = [
            ("data", ("data.json", data_file, "application/json")),
            ("data_archive", ("data.tar.gz", fp, "application/x-gtar")),
        ]

        requests.post(url, files=files)
