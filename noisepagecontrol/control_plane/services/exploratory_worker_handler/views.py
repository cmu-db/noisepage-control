import json
import logging
from threading import Thread

from control_plane.services.event_queue.event_types import EventType
from control_plane.services.event_queue.producer import publish_event
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .exploratory_pg_status_types import ExploratoryPGStatusType
from .models import ExploratoryPGInfo
from .save_collected_data import save_collected_data

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
def launch_exploratory_postgres_callback(request):
    data = json.loads(request.body)
    tuning_id = data["tuning_id"]
    event_name = data["event_name"]
    exploratory_postgres_port = data["exploratory_postgres_port"]

    logger.info(f"Received ack from launching exploratory cluster: f{json.dumps(data)}")

    # Update exploratory PG status, store port number
    exploratoy_pg_info = ExploratoryPGInfo.objects.get(
        tuning_id=tuning_id, launch_event_name=event_name
    )
    exploratoy_pg_info.exploratory_pg_port = exploratory_postgres_port
    exploratoy_pg_info.status = ExploratoryPGStatusType.READY
    exploratoy_pg_info.save()

    publish_event(
        event_type=EventType.LAUNCH_EXPLORATORY_POSTGRES,
        data={"tuning_id": tuning_id, "event_name": event_name},
        completed=True,
    )

    return HttpResponse()


@csrf_exempt
@require_http_methods(["POST"])
def data_collector_callback(request):

    data = json.loads(request.FILES["data"].read().decode("utf-8"))

    tuning_id = data["tuning_id"]
    resource_id = data["resource_id"]
    event_name = data["event_name"]

    logger.info(
        "Received collected data. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    collected_data_tar = request.FILES["data_archive"].read()
    collected_data_filename = request.FILES["data_archive"].name

    # Start workload save on a new thread; allow request to return
    thread = Thread(
        target=save_collected_data,
        args=(
            tuning_id,
            resource_id,
            collected_data_tar,
            collected_data_filename,
            event_name,
        ),
    )
    thread.start()

    return HttpResponse("OK")
