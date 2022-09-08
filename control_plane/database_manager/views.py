from django.http import HttpResponse

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from environment_manager.environment_types import EnvironmentType

from .models import Database
from .database_state_types import DatabaseStateType

import json

import paramiko
from paramiko.client import SSHClient


@csrf_exempt
@require_http_methods(["GET"])
def list_databases(request):

    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname = "ec2-18-217-99-54.us-east-2.compute.amazonaws.com",
        port = 22,
        username = "ubuntu",
        key_filename = "./resources/keys/test.pem",
        timeout = 30,
    )

    stdin, stdout, stderr = client.exec_command('sudo -v')
    print (stdin, stdout, stderr)

    stdout=stdout.read()
    print (stdout)
    client.close()

    return HttpResponse("Hello, world. This is all databases view")


@csrf_exempt
@require_http_methods(["POST"])
def register_database(request):

    data = json.loads(request.body)

    if "environment" not in data:
        return HttpResponse('No environment specified', status=403)

    environment = data["environment"]

    # Create a new intsance
    new_database = Database(
        environment_type = environment,
        state = DatabaseStateType.REGISTERING,
    )

    # Load up config
    if environment == EnvironmentType.SELF_MANAGED_POSTGRES:
        if "self_managed_postgres_config" not in data:
            return HttpResponse('"self_managed_postgres_config" not specified', status=403)
        config = data["self_managed_postgres_config"]

        if not is_self_managed_postgress_config_valid(config):
            return HttpResponse('invalid config', status=403)

        new_database.self_managed_postgres_config = config

    elif environment == EnvironmentType.AWS_RDS_POSTGRES:
        if "aws_rds_postgres_config" not in data:
            return HttpResponse('"aws_rds_postgres_config" not specified', status=403)
        new_database.self_managed_postgres_config = data["aws_rds_postgres_config"]
    else:
        return HttpResponse('Unrecognised environment', status=403)
    
    new_database.save()

    return HttpResponse(
        serializers.serialize(
            "json",
            [
                new_database,
            ],
        ),
        content_type="application/json",
    )



self_managed_postgres_config_keys = [
    "primary_host", "primary_ssh_port", "primary_ssh_user", "primary_pem_key", "primary_pg_user", "primary_pg_port",
    "replica_host", "replica_ssh_port", "replica_ssh_user", "replica_pem_key", "replica_pg_user", "replica_pg_port"
]

def is_self_managed_postgress_config_valid(config):
    for key in self_managed_postgres_config_keys:
        if key not in config:
            return False

    return True