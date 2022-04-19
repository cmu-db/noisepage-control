import json
import logging

import requests
from control_plane.services.resource_manager.initialise_resource import (
    initialise_resource,
)
from control_plane.services.resource_manager.resource_type import ResourceType
from django.conf import settings

logger = logging.getLogger("control_plane")


def collect_data_from_exploratory(
    tuning_id,
    event_name,
    replica_url,
    postgres_port,
    data_collector_type,
    data_collector_config,
):
    logger.info(f"Sending request to collect data. Event name: {event_name}")

    # Initialise a new resource for this workload
    resource_id = initialise_resource(tuning_id, ResourceType.EXPLORATORY_DATA)

    url = "http://%s:%s/collect_data/" % (
        replica_url,
        settings.EXPLORATORY_WORKER_PORT,
    )

    data = {
        "resource_id": resource_id,
        "event_name": event_name,
        "postgres_port": postgres_port,
        "data_collector_type": data_collector_type,
        "config": data_collector_config,
    }

    headers = {"Content-type": "application/json"}
    requests.post(url, data=json.dumps(data), headers=headers)
