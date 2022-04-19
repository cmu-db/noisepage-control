import json
import time
from threading import Thread

import requests
from django.apps import AppConfig
from django.conf import settings


def send_service_ready_to_control_plane():

    # Wait for some time before sending the ack
    time.sleep(10)

    control_plane_url = settings.CONTROL_PLANE_URL
    control_plane_port = settings.CONTROL_PLANE_PORT
    tuning_id = settings.TUNING_ID
    command_name = settings.LAUNCH_COMMAND_NAME

    url = "http://%s:%s/primary_worker_handler/healthcheck/" % (
        control_plane_url,
        control_plane_port,
    )
    data = {"tuning_id": tuning_id, "command_name": command_name}
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    requests.post(url, data=json.dumps(data), headers=headers)


class PrimaryWorkerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "primary_worker"

    def ready(self):
        """
        Send healthcheck to control plane on ready
        TODO: Add robustness
        """

        thread = Thread(target=send_service_ready_to_control_plane)
        thread.start()
