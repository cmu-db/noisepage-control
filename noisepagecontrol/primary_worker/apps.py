import json
import requests

from django.conf import settings
from django.apps import AppConfig


class PrimaryWorkerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "primary_worker"

    def ready(self):
        """
        Send healthcheck to control plane on ready
        TODO: Add robustness
        """

        control_plane_url = settings.CONTROL_PLANE_URL
        control_plane_port = settings.CONTROL_PLANE_PORT
        tuning_id = settings.TUNING_ID
        event_name = settings.LAUNCH_EVENT_NAME

        url = "http://%s:%s/primary_worker_handler/healthcheck" % (
            control_plane_url,
            control_plane_port,
        )
        data = {"tuning_id": tuning_id, "event_name": event_name}
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        requests.post(url, data=json.dumps(data), headers=headers)
