import json
import logging
import requests

from django.conf import settings

logger = logging.getLogger("control_plane")


def launch_exploratory_postgres(tuning_id, event_name):
    from control_plane.services.tuning_manager.models import TuningInstance, TuningEvent

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)
    tuning_event = TuningEvent.objects.get(tuning_id=tuning_id, event_name=event_name)

    # Get config.snapshot to decide if exploratory postgres cluster should be
    # launched by taking a snapshot of replica cluster. Default to false.
    snapshot = tuning_event.config.get("snapshot", False)

    logger.info(
        "Sending request to launch exploratory postgres cluster. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    url = "http://%s:%s/launch_exploratory_cluster/" % (
        tuning_instance.replica_url,
        settings.EXPLORATORY_WORKER_PORT,
    )

    data = {"event_name": event_name, "snapshot": snapshot}

    headers = {"Content-type": "application/json"}
    requests.post(url, data=json.dumps(data), headers=headers)
