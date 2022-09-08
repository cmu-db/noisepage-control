import uuid 

from django.db import models
from django.core.exceptions import ValidationError

from environment_manager.environment_types import EnvironmentType
from django.contrib.postgres.fields import JSONField

from .database_state_types import DatabaseStateType

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
    active = models.BooleanField(default=False)

    """
        - primary_host
        - primary_ssh_port
        - primary_ssh_user
        - primary_pem_key
        - primary_pg_user
        - primary_pg_port

        - replica_host
        - replica_ssh_port
        - replica_ssh_user
        - replica_pem_key
        - replica_pg_user
        - replica_pg_port

    """
    self_managed_postgres_config = models.JSONField(default=dict)

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



