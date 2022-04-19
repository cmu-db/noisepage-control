from django.db import models

from .exploratory_pg_status_types import ExploratoryPGStatusType


class ExploratoryPGInfo(models.Model):
    tuning_id = models.CharField(max_length=36)

    # The command name that launches the exploratory PG cluster
    launch_command_name = models.CharField(max_length=120)
    exploratory_pg_port = models.IntegerField(null=True)

    STATUS_CHOICES = [
        # Exploratory PG launching request sent
        (ExploratoryPGStatusType.PENDING, "PENDING"),
        # Received launch exploratory PG callback and port
        (ExploratoryPGStatusType.READY, "READY"),
        # Exploratory PG cluster stopped
        (ExploratoryPGStatusType.STOPPED, "STOPPED"),
    ]

    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
