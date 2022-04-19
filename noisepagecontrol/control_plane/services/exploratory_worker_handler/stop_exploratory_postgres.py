import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger("control_plane")


def stop_exploratory_postgres(replica_url, port):
    logger.info(
        f"Sending request to stop exploratory cluster. replica_url: {replica_url}, port: {port}"
    )
    url = "http://%s:%s/stop_exploratory_postgres/" % (
        replica_url,
        settings.EXPLORATORY_WORKER_PORT,
    )

    data = {"port": port}
    headers = {"Content-type": "application/json"}
    requests.delete(url, data=json.dumps(data), headers=headers)
