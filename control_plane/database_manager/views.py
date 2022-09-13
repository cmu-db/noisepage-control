from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from environments.environment_types import EnvironmentType
from resource_manager.resource_type import ResourceType
from resource_manager.views import (
    initialise_resource,
    initialise_resource_dir,
    save_resource,
)

from .database_state_types import DatabaseStateType
from .models import Database, SelfManagedPostgresConfig
from .services.command_queue.command_types import CommandType
from .services.command_queue.models import Command
from .services.command_queue.producer import publish_command


@csrf_exempt
@require_http_methods(["GET"])
def list_databases(request):

    return render(request, "index.html", context={})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def register_database(request):
    if request.method == "POST":
        return register_new_database(request)
    return render(request, "register_database.html", context={})


"""
    Registers a new database
    1. Creates db entries
    2. Inits resource directory
    3. Fires off registration command
"""


def register_new_database(request):

    if "environment" not in request.POST:
        return HttpResponse("Unrecognised environment", status=403)
    environment = request.POST["environment"]

    # Create a new intsance
    new_database = Database(
        environment_type=environment,
        state=DatabaseStateType.REGISTERING,
    )
    new_database.save()

    # Init resource dir for database
    initialise_resource_dir(new_database.database_id)

    # Load up config
    if environment == EnvironmentType.SELF_MANAGED_POSTGRES:
        if not is_self_managed_postgress_config_valid(request.POST):
            return HttpResponse("Invalid config", status=403)

        register_new_self_managed_postgres_database(request, new_database)

    elif environment == EnvironmentType.AWS_RDS_POSTGRES:
        pass
    else:
        return HttpResponse("Unrecognised environment", status=403)

    # Fire register database command
    new_command = Command(
        command_type=CommandType.REGISTER_DATABASE,
        parent_command_ids=[],
        database_id=new_database.database_id,
        completed=False,
    )
    new_command.save()

    publish_command(
        new_command.command_type, new_command.command_id, new_command.database_id, {}
    )

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
    "primary_host",
    "primary_ssh_port",
    "primary_ssh_user",
    "primary_pg_user",
    "primary_pg_port",
    "replica_host",
    "replica_ssh_port",
    "replica_ssh_user",
    "replica_pg_user",
    "replica_pg_port",
]


def is_self_managed_postgress_config_valid(config):
    for key in self_managed_postgres_config_keys:
        if key not in config:
            return False

    return True


def register_new_self_managed_postgres_database(request, database):

    # Save primary key
    resource_id = initialise_resource(database.database_id, ResourceType.KEY)
    primary_key_resource = save_resource(
        database.database_id,
        resource_id,
        request.FILES["primary_key_file"].read(),
        "primary_key.pem",
    )

    # Save replica key
    resource_id = initialise_resource(database.database_id, ResourceType.KEY)
    replica_key_resource = save_resource(
        database.database_id,
        resource_id,
        request.FILES["replica_key_file"].read(),
        "replica_key.pem",
    )

    config = SelfManagedPostgresConfig(
        database=database,
        primary_host=request.POST["primary_host"],
        primary_ssh_port=request.POST["primary_ssh_port"],
        primary_ssh_user=request.POST["primary_ssh_user"],
        primary_pg_user=request.POST["primary_pg_user"],
        primary_pg_port=request.POST["primary_pg_port"],
        replica_host=request.POST["replica_host"],
        replica_ssh_port=request.POST["replica_ssh_port"],
        replica_ssh_user=request.POST["replica_ssh_user"],
        replica_pg_user=request.POST["replica_pg_user"],
        replica_pg_port=request.POST["replica_pg_port"],
        primary_ssh_key=primary_key_resource,
        replica_ssh_key=replica_key_resource,
    )

    config.save()
