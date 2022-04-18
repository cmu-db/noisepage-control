import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from .resource_type import ResourceType


def autogenerate_uuid():
    return str(uuid.uuid4())


class Resource(models.Model):

    resource_id = models.CharField(max_length=36, default=autogenerate_uuid)
    tuning_id = models.CharField(max_length=36)

    RESOURCE_TYPE_CHOICES = [
        (ResourceType.WORKLOAD, "Workload"),
        (ResourceType.TRAINING_DATA, "Training Data"),
    ]

    resource_type = models.CharField(max_length=32, choices=RESOURCE_TYPE_CHOICES)

    # Whether the resource is available to be used
    available = models.BooleanField(default=False)

    # The file name of the resource
    resource_name = models.CharField(max_length=120, blank=True)
