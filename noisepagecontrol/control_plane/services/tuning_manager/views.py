import json
import uuid

from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from control_plane.models import TuningInstance
from control_plane.services.event_queue.event_types import EventType
from control_plane.services.event_queue.event_handler_types import EventHandlerType
from control_plane.services.event_queue.producer import publish_event


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

    # 2. Publish events to launch primary worker
    publish_event(
        event_type=EventType.LAUNCH_PRIMARY_WORKER,
        event_handler=EventHandlerType.PRIMARY_WORKER_HANDLER,
        data={"tuning_uuid": new_tuning_request.uuid},
    )

    # 3. Publish events to launch exploratory worker
    publish_event(
        event_type=EventType.LAUNCH_EXPLORATORY_WORKER,
        event_handler=EventHandlerType.EXPLORATORY_WORKER_HANDLER,
        data={"tuning_uuid": new_tuning_request.uuid},
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
