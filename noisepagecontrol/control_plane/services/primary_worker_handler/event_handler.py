from control_plane.services.event_queue.event_types import EventType

from .capture_primary_workload import capture_primary_workload
from .launch_primary_worker import launch_primary_worker


def handle_event(event):

    event_type = event["event_type"]

    if event_type == EventType.LAUNCH_PRIMARY_WORKER:
        handle_launch_primary_worker_event(event)
    elif event_type == EventType.CAPTURE_PRIMARY_WORKLOAD:
        handle_capture_primary_workload_event(event)


def handle_launch_primary_worker_event(event):

    tuning_id = event["data"]["tuning_id"]
    event_name = event["data"]["event_name"]

    """
        Fetch associated tuning instance. 
        We need to pass primary port to the launched worker
    """
    from control_plane.services.tuning_manager.models import TuningInstance

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)

    launch_primary_worker(
        tuning_id,
        tuning_instance.primary_port,
        tuning_instance.primary_username,
        event_name,
    )


def handle_capture_primary_workload_event(event):

    tuning_id = event["data"]["tuning_id"]
    event_name = event["data"]["event_name"]
    capture_primary_workload(tuning_id, event_name)
