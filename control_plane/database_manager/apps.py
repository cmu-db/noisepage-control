from threading import Thread

from database_manager.services.command_queue.consumer import (
    init_command_consumer,
)
from django.apps import AppConfig


class DatabaseManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "database_manager"

    def ready(self):
        """
        Init command consumer

        TODO: Add robustness to the consumer thread.
        What happens if it fails?
        """

        thread = Thread(target=init_command_consumer)
        thread.start()
