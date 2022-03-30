import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField


def tuningInstance_state_default():
    return {}


def autogenerate_uuid():
    return str(uuid.uuid4())


# Create your models here.
class TuningInstance(models.Model):

    primary_url = models.CharField(max_length=30)
    primary_port = models.CharField(max_length=5)
    replica_url = models.CharField(max_length=30)
    replica_port = models.CharField(max_length=5)

    state = models.JSONField("state", default=tuningInstance_state_default)

    # Unique identifier for this tuning request
    tuning_id = models.CharField(max_length=36, primary_key=True, default=autogenerate_uuid)
    

class TuningEvent(models.Model):

    event_name = models.CharField(max_length=120)
    event_type = models.CharField(max_length=120)
    parent_event_names = ArrayField(models.CharField(max_length=120), blank=True)
    tuning_id = models.CharField(max_length=36)
    completed = models.BooleanField(default=False)