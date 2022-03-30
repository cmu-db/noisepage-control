import os
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from control_plane.services.event_queue.producer import publish_event
from control_plane.services.event_queue.event_types import EventType
from control_plane.services.event_queue.event_handler_types import EventHandlerType
from control_plane.services.event_queue.event_handler_mapping import EventHandlerMapping


def index(request):
    return HttpResponse("Hello, world. This is the primary worker handler")


# The primary worker calls this view to acknowledging that its running
@csrf_exempt
@require_http_methods(["POST"])
def healthcheck(request):

    data = json.loads(request.body)
    tuning_id = data["tuning_id"]
    event_name = data["event_name"]
    print("Received HC from primary worker", tuning_id, event_name)

    # Publish LAUNCH_PRIMARY_WORKER event as completed
    publish_event(
        event_type=EventType.LAUNCH_PRIMARY_WORKER,
        event_handler=EventHandlerMapping[EventType.LAUNCH_PRIMARY_WORKER],
        data={"tuning_id": tuning_id, "event_name": event_name},
        completed=True,
    )

    return HttpResponse("OK")


# TODO: Need to do checks here to prevent double spawning
# TODO: Mark this as a celery task when spawning across machines
def launch_primary_worker(tuning_id, event_name):
    print("Launching primary for", tuning_id, event_name)

    # Very hacky way of passing env vars and launching
    # Needs to be reworked when we move workers away from local
    os.spawnvpe(
        os.P_NOWAIT,
        "pipenv",
        ["pipenv", "run", "./run.sh", "PRIMARY_WORKER"],
        env={
            **os.environ,
            "TUNING_ID": tuning_id,
            "CONTROL_PLANE_URL": "127.0.0.1",
            "CONTROL_PLANE_PORT": "8000",
            "LAUNCH_EVENT_NAME": event_name,
        },
    )
