import json

from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from control_plane.services.event_queue.producer import publish_event

from .models import TuningInstance, TuningEvent


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

    # This tracks events which do not have any parent events
    # They will be executed immediately
    initial_events = []
    # Add constraints and validations here!!
    for event in tune_db_request_data["event_config"]:
        new_event = TuningEvent(
            event_type=event["event_type"],
            event_name=event["event_name"],
            parent_event_names=event["parent_event_names"],
            tuning_id=new_tuning_request.tuning_id,
            config=event.get("config", {}),
            completed=False,
        )
        new_event.save()
        if len(new_event.parent_event_names) == 0:
            initial_events.append(new_event)

    # Publish initial events
    for initial_event in initial_events:
        publish_event(
            event_type=initial_event.event_type,
            data={
                "tuning_id": new_tuning_request.tuning_id,
                "event_name": initial_event.event_name,
                "config": initial_event.config,
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
