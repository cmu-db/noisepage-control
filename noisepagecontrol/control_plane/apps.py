from threading import Thread

from control_plane.services.event_queue.consumer import init_event_consumer
from django.apps import AppConfig


class ControlPlaneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "control_plane"

    def ready(self):
        """
        Init event consumer

        TODO: Add robustness to the consumer thread.
        What happens if it fails?
        """

        thread = Thread(target=init_event_consumer)
        thread.start()
