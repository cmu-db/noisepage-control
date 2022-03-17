import json
import requests

from django.conf import settings
from django.apps import AppConfig


class ExploratoryWorkerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exploratory_worker"

    def ready(self):
        """
        Send healthcheck to control plane on ready
        TODO: Add robustness
        """

        control_plane_url = settings.CONTROL_PLANE_URL
        control_plane_port = settings.CONTROL_PLANE_PORT
        tuning_id = settings.TUNING_ID

        url = "http://%s:%s/exploratory_worker_handler/healthcheck" % (
            control_plane_url,
            control_plane_port,
        )
        data = {"tuning_uuid": tuning_id}
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        requests.post(url, data=json.dumps(data), headers=headers)
