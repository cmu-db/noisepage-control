import json
import logging
import requests
import time

from threading import Thread

from django.conf import settings
from django.apps import AppConfig

logger = logging.getLogger("exploratory_worker")


def send_service_ready_to_control_plane():
    # Wait for some time before sending the ack
    logger.info("Wait for some time before sending the ack")
    time.sleep(10)

    control_plane_url = settings.CONTROL_PLANE_URL
    control_plane_port = settings.CONTROL_PLANE_PORT
    tuning_id = settings.TUNING_ID
    event_name = settings.LAUNCH_EVENT_NAME

    url = "http://%s:%s/exploratory_worker_handler/healthcheck/" % (
        control_plane_url,
        control_plane_port,
    )
    data = {"tuning_id": tuning_id, "event_name": event_name}
    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    logger.info("Sending exploratory worker ready message to control plane")
    requests.post(url, data=json.dumps(data), headers=headers)


class ExploratoryWorkerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exploratory_worker"

    def ready(self):
        """
        Send healthcheck to control plane on ready
        TODO: Add robustness
        """
        thread = Thread(target=send_service_ready_to_control_plane)
        thread.start()
