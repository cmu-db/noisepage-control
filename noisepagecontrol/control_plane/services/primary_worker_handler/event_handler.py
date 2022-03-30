from control_plane.services.event_queue.event_types import EventType

from .views import launch_primary_worker


def handle_event(event):

    event_type = event["event_type"]

    if event_type == EventType.LAUNCH_PRIMARY_WORKER:
        handle_launch_primary_worker_event(event)


def handle_launch_primary_worker_event(event):

    tuning_id = event["data"]["tuning_id"]
    event_name = event["data"]["event_name"]
    launch_primary_worker(tuning_id, event_name)
