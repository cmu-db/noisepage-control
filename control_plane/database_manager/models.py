import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from environments.environment_types import EnvironmentType
from resource_manager.models import Resource

from .database_state_types import DatabaseStateType


def autogenerate_uuid():
    return str(uuid.uuid4())


class Database(models.Model):

    database_id = models.CharField(
        max_length=36, primary_key=True, default=autogenerate_uuid
    )

    ENVIRONMENT_TYPE_CHOICES = [
        (EnvironmentType.SELF_MANAGED_POSTGRES, "Self managed postgres"),
        (EnvironmentType.AWS_RDS_POSTGRES, "AWS RDS Postgres"),
    ]
    environment_type = models.CharField(
        max_length=120, choices=ENVIRONMENT_TYPE_CHOICES
    )

    # Whether the resource is active or removed
    active = models.BooleanField(default=True)

    DATABSE_STATE_CHOICES = [
        (DatabaseStateType.REGISTERING, "REGISTERING"),
        (DatabaseStateType.HEALTHY, "HEALTHY"),
        (DatabaseStateType.UNHEALTHY, "UNHEALTHY"),
        (DatabaseStateType.TUNING, "TUNING"),
        (DatabaseStateType.COLLECTING_WORKLOAD, "COLLECTING_WORKLOAD"),
        (DatabaseStateType.COLLECTING_METRICS, "COLLECTING_METRICS"),
        (DatabaseStateType.COLLECTING_STATE, "COLLECTING_STATE"),
    ]
    state = models.CharField(max_length=120, choices=DATABSE_STATE_CHOICES)

    errors = ArrayField(models.TextField(), blank=True, default=list)


class SelfManagedPostgresConfig(models.Model):

    database = models.OneToOneField(
        Database, on_delete=models.CASCADE, primary_key=True
    )

    primary_host = models.CharField(max_length=120, blank=False, null=False)
    primary_ssh_port = models.CharField(max_length=120, blank=False, null=False)
    primary_ssh_user = models.CharField(max_length=120, blank=False, null=False)
    primary_pg_user = models.CharField(max_length=120, blank=False, null=False)
    primary_pg_port = models.CharField(max_length=120, blank=False, null=False)

    replica_host = models.CharField(max_length=120, blank=False, null=False)
    replica_ssh_port = models.CharField(max_length=120, blank=False, null=False)
    replica_ssh_user = models.CharField(max_length=120, blank=False, null=False)
    replica_pg_user = models.CharField(max_length=120, blank=False, null=False)
    replica_pg_port = models.CharField(max_length=120, blank=False, null=False)

    primary_ssh_key = models.OneToOneField(
        Resource, on_delete=models.CASCADE, related_name="primary_ssh_key"
    )
    replica_ssh_key = models.OneToOneField(
        Resource, on_delete=models.CASCADE, related_name="replica_ssh_key"
    )
