import os
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from control_plane.services.event_queue.producer import publish_event
from control_plane.services.event_queue.event_handler_types import EventHandlerType
from control_plane.services.event_queue.event_types import EventType


def index(request):
    return HttpResponse("Hello, world. This is the primary worker handler")


# The primary worker calls this view to acknowledging that its running
@csrf_exempt
@require_http_methods(["POST"])
def healthcheck(request):

    data = json.loads(request.body)
    tuning_uuid = data["tuning_uuid"]
    print("Received HC from primary worker", tuning_uuid)

    # Publish primary worker ready event
    publish_event(
        event_type=EventType.PRIMARY_WORKER_READY,
        event_handler=EventHandlerType.TUNING_MANAGER,
        data={"tuning_uuid": tuning_uuid},
    )

    return HttpResponse("OK")


# TODO: Need to do checks here to prevent double spawning
# TODO: Mark this as a celery task when spawning across machines
def launch_primary_worker(tuning_uuid):
    print("Launching primary for", tuning_uuid)

    # Very hacky way of passing env vars and launching
    # Needs to be reworked when we move workers away from local
    os.spawnvpe(
        os.P_NOWAIT,
        "pipenv",
        ["pipenv", "run", "./run.sh", "PRIMARY_WORKER"],
        env={
            **os.environ,
            "TUNING_ID": tuning_uuid,
            "CONTROL_PLANE_URL": "127.0.0.1",
            "CONTROL_PLANE_PORT": "8000",
        },
    )
