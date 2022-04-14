import json
import logging
import requests

from django.conf import settings

from control_plane.services.resource_manager.workload_resource_handler import (
    initialise_workload_resource,
)

logger = logging.getLogger("control_plane")


def capture_primary_workload(tuning_id, event_name):

    # Fetch associated tuning instance and tuning event
    from control_plane.services.tuning_manager.models import TuningInstance, TuningEvent

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)
    tuning_event = TuningEvent.objects.get(tuning_id=tuning_id, event_name=event_name)

    # Get time period for capturing workload; default to 5 seconds
    time_period = tuning_event.config.get("time_period", 5)

    # Initialise a new resource for this workload
    resource_id = initialise_workload_resource(tuning_id)

    logger.info(
        "Sending request to capture workload. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    url = "http://%s:%s/capture_workload/" % (
        tuning_instance.primary_url,
        settings.PRIMARY_WORKER_PORT,
    )

    data = {
        "tuning_id": tuning_id,
        "resource_id": resource_id,
        "event_name": event_name,
        "time_period": time_period,
    }

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    requests.post(url, data=json.dumps(data), headers=headers)
