import uuid

def autogenerate_uuid():
    return str(uuid.uuid4())

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Command(models.Model):
    
    command_id = models.CharField(max_length=36, primary_key=True, default=autogenerate_uuid)
    database_id = models.CharField(max_length=36)
    parent_command_ids = ArrayField(models.CharField(max_length=36), blank=True)

    command_type = models.CharField(max_length=120)

    completed = models.BooleanField(default=False)
    config = models.JSONField("config", default = dict)
