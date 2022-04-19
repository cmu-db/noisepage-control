import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


def get_empty_object():
    return {}


def autogenerate_uuid():
    return str(uuid.uuid4())


class TuningInstance(models.Model):

    primary_url = models.CharField(max_length=120)
    primary_port = models.CharField(max_length=5)
    replica_url = models.CharField(max_length=120)
    replica_port = models.CharField(max_length=5)

    state = models.JSONField("state", default=get_empty_object)

    # Unique identifier for this tuning request
    tuning_id = models.CharField(
        max_length=36, primary_key=True, default=autogenerate_uuid
    )


class TuningCommand(models.Model):

    command_name = models.CharField(max_length=120)
    command_type = models.CharField(max_length=120)
    parent_command_names = ArrayField(models.CharField(max_length=120), blank=True)
    tuning_id = models.CharField(max_length=36)
    completed = models.BooleanField(default=False)
    config = models.JSONField("config", default=get_empty_object)
