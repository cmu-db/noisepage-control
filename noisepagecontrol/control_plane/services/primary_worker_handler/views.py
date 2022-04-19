import json
import logging
from threading import Thread

from control_plane.services.event_queue.event_types import EventType
from control_plane.services.event_queue.producer import publish_event
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .save_captured_workload import save_captured_workload

logger = logging.getLogger("control_plane")


def index(request):
    return HttpResponse("Hello, world. This is the primary worker handler")


# The primary worker calls this view to acknowledging that its running
@csrf_exempt
@require_http_methods(["POST"])
def healthcheck(request):

    data = json.loads(request.body)
    tuning_id = data["tuning_id"]
    event_name = data["event_name"]
    logger.info(
        "Received HC from primary worker. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    # Publish LAUNCH_PRIMARY_WORKER event as completed
    publish_event(
        event_type=EventType.LAUNCH_PRIMARY_WORKER,
        data={"tuning_id": tuning_id, "event_name": event_name},
        completed=True,
    )

    return HttpResponse("OK")


@csrf_exempt
@require_http_methods(["POST"])
def workload_capture_callback(request):

    data = json.loads(request.FILES["data"].read().decode("utf-8"))

    tuning_id = data["tuning_id"]
    resource_id = data["resource_id"]
    event_name = data["event_name"]

    logger.info(
        "Received captured workload. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    captured_workload_tar = request.FILES["workload"].read()
    captured_workload_filename = request.FILES["workload"].name

    # Start workload save on a new thread; allow request to return
    thread = Thread(
        target=save_captured_workload,
        args=(
            tuning_id,
            resource_id,
            captured_workload_tar,
            captured_workload_filename,
            event_name,
        ),
    )
    thread.start()

    return HttpResponse("OK")
