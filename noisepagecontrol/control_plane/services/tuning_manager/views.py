import json

from control_plane.services.command_queue.producer import publish_command
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import TuningCommand, TuningInstance


def index(request):
    return HttpResponse("Hello, world. This is the control_plane tuning manager")


@csrf_exempt
@require_http_methods(["POST"])
def tune_database(request):

    # 1. Create a new tuning instance
    tune_db_request_data = json.loads(request.body)

    # TODO: Requires validations!!
    new_tuning_request = TuningInstance(
        primary_url=tune_db_request_data["primary_url"],
        primary_port=str(tune_db_request_data["primary_port"]),
        replica_url=tune_db_request_data["replica_url"],
        replica_port=str(tune_db_request_data["replica_port"]),
        state={"primary_worker_ready": False, "exploratory_worker_ready": False},
    )
    new_tuning_request.save()

    # This tracks commands which do not have any parent commands
    # They will be executed immediately
    initial_commands = []
    # Add constraints and validations here!!
    for command in tune_db_request_data["command_config"]:
        new_command = TuningCommand(
            command_type=command["command_type"],
            command_name=command["command_name"],
            parent_command_names=command["parent_command_names"],
            tuning_id=new_tuning_request.tuning_id,
            config=command.get("config", {}),
            completed=False,
        )
        new_command.save()
        if len(new_command.parent_command_names) == 0:
            initial_commands.append(new_command)

    # Publish initial commands
    for initial_command in initial_commands:
        publish_command(
            command_type=initial_command.command_type,
            data={
                "tuning_id": new_tuning_request.tuning_id,
                "command_name": initial_command.command_name,
                "config": initial_command.config,
            },
            completed=False,
        )

    return HttpResponse(
        serializers.serialize(
            "json",
            [
                new_tuning_request,
            ],
        ),
        content_type="application/json",
    )
