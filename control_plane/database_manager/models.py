import uuid 
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError

from environments.environment_types import EnvironmentType
from django.contrib.postgres.fields import ArrayField

from .database_state_types import DatabaseStateType

from .services.command_queue.models import Command
from resource_manager.models import Resource
from .types.tuningstatus import TuningStatusType
from .types.action_status import ActionStatusType

def autogenerate_uuid():
    return str(uuid.uuid4())

class Database(models.Model):

    database_id = models.CharField(max_length=36, primary_key=True, default=autogenerate_uuid)

    ENVIRONMENT_TYPE_CHOICES = [
        (EnvironmentType.SELF_MANAGED_POSTGRES, "Self managed postgres"),
        (EnvironmentType.AWS_RDS_POSTGRES, "AWS RDS Postgres"),
    ]
    environment_type = models.CharField(max_length=120, choices=ENVIRONMENT_TYPE_CHOICES)

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

    errors = ArrayField(models.TextField(), blank=True, default = list)
    
    created = models.DateTimeField(auto_now_add=True)



class SelfManagedPostgresConfig(models.Model):

    database = models.OneToOneField(
        Database, on_delete=models.CASCADE, primary_key=True)

    db_name = models.CharField(max_length=120, blank = False, null = False)
    primary_host = models.CharField(max_length=120, blank = False, null = False)
    primary_ssh_port = models.CharField(max_length=120, blank = False, null = False)
    primary_ssh_user = models.CharField(max_length=120, blank = False, null = False)
    primary_pg_user = models.CharField(max_length=120, blank = False, null = False)
    primary_pg_port = models.CharField(max_length=120, blank = False, null = False)

    replica_host = models.CharField(max_length=120, blank = False, null = False)
    replica_ssh_port = models.CharField(max_length=120, blank = False, null = False)
    replica_ssh_user = models.CharField(max_length=120, blank = False, null = False)
    replica_pg_user = models.CharField(max_length=120, blank = False, null = False)
    replica_pg_port = models.CharField(max_length=120, blank = False, null = False)

    primary_ssh_key = models.OneToOneField(
        Resource, on_delete=models.CASCADE, related_name = "primary_ssh_key")
    replica_ssh_key = models.OneToOneField(
        Resource, on_delete=models.CASCADE, related_name = "replica_ssh_key")


class TuningInstance(models.Model):
    tuning_instance_id = models.CharField(max_length=36, default=autogenerate_uuid)
    database_id = models.CharField(max_length=36)
    friendly_name = models.CharField(max_length=512, unique=True)

    # The workload and state used to generate this tuning instance
    workload_id = models.CharField(max_length=36)
    state_id = models.CharField(max_length=36)

    TUNING_STATUS_CHOICES = [
        (TuningStatusType.RUNNING, "RUNNING"),
        (TuningStatusType.FINISHED, "FINISHED"),
        (TuningStatusType.FAILED, "FAILED"),
    ]

    status = models.CharField(max_length=32, choices=TUNING_STATUS_CHOICES)

    # When the tuning finished
    finished_at = models.DateTimeField(blank = True)

    # The file name of the action
    action_name = models.CharField(max_length=120, blank=True)

class TuningAction(models.Model):
    tuning_action_id = models.CharField(max_length=36, default=autogenerate_uuid)

    # The database
    database_id = models.CharField(max_length=36)

    # The tuning instance that generated this action
    tuning_instance_id = models.CharField(max_length=36)

    # The command; CREATE INDEX ...
    command = models.CharField(max_length=512)

    # The benefit that would result from applying this action
    benefit = models.FloatField()

    # Whether the database has to be rebooted after applying the action
    reboot_required = models.BooleanField(default=False)

    ACTION_STATUS_CHOICES = [
        (ActionStatusType.NOT_APPLIED, "NOT_APPLIED"),
        (ActionStatusType.APPLYING, "APPLYING"),
        (ActionStatusType.APPLIED, "APPLIED"),
        (ActionStatusType.FAILED, "FAILED"),
    ]

    status = models.CharField(max_length=32, choices=ACTION_STATUS_CHOICES)
