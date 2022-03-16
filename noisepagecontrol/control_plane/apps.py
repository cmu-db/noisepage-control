from django.apps import AppConfig
from control_plane.services.event_queue.consumer import init_message_consumer
from threading import Thread


class ControlPlaneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "control_plane"

    """
        Init message consumer

        TODO: Add robustness to the consumer thread. 
        What happens if it fails?
    """

    def ready(self):
        thread = Thread(target=init_message_consumer)
        thread.start()
