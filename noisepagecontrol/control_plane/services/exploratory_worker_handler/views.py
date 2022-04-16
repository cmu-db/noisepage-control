import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from control_plane.services.event_queue.producer import publish_event
from control_plane.services.event_queue.event_handler_types import EventHandlerType
from control_plane.services.event_queue.event_types import EventType
from control_plane.services.event_queue.event_handler_mapping import EventHandlerMapping

logger = logging.getLogger("control_plane")


def index(request):
    return HttpResponse("Hello, world. This is the exploratory worker handler")


# The exploratory worker calls this view to acknowledging that its running
@csrf_exempt
@require_http_methods(["POST"])
def healthcheck(request):

    data = json.loads(request.body)
    tuning_id = data["tuning_id"]
    event_name = data["event_name"]

    logger.info(
        "Received HC from exporatory worker. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    # Publish LAUNCH_EXPLORATORY_WORKER event as completed
    publish_event(
        event_type=EventType.LAUNCH_EXPLORATORY_WORKER,
        data={"tuning_id": tuning_id, "event_name": event_name},
        completed=True,
    )

    return HttpResponse("OK")


@csrf_exempt
@require_http_methods(["POST"])
def launch_exploratory_cluster_callback(request):
    data = json.loads(request.body)
    tuning_id = data["tuning_id"]
    event_name = data["event_name"]

    logger.info(
        "Received ack from launching exploratory cluster. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    publish_event(
        event_type=EventType.LAUNCH_EXPLORATORY_POSTGRES,
        data={"tuning_id": tuning_id, "event_name": event_name},
        completed=True,
    )

    return HttpResponse()
