import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger("control_plane")


def launch_exploratory_postgres(command_name, replica_url, snapshot):
    logger.info(
        f"Sending request to launch exploratory postgres cluster. Command name: {command_name}"
    )

    url = "http://%s:%s/launch_exploratory_postgres/" % (
        replica_url,
        settings.EXPLORATORY_WORKER_PORT,
    )

    data = {"command_name": command_name, "snapshot": snapshot}

    headers = {"Content-type": "application/json"}
    requests.post(url, data=json.dumps(data), headers=headers)
