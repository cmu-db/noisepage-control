from threading import Thread

from control_plane.services.command_queue.consumer import init_command_consumer
from django.apps import AppConfig


class ControlPlaneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "control_plane"

    def ready(self):
        """
        Init command consumer

        TODO: Add robustness to the consumer thread.
        What happens if it fails?
        """

        thread = Thread(target=init_command_consumer)
        thread.start()
