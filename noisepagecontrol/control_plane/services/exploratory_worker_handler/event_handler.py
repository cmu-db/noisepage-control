from control_plane.services.event_queue.event_types import EventType

from .views import launch_exploratory_worker


def handle_event(event):

    event_type = event["event_type"]

    if event_type == EventType.LAUNCH_EXPLORATORY_WORKER:
        handle_launch_exploratory_worker_event(event)


def handle_launch_exploratory_worker_event(event):

    tuning_id = event["data"]["tuning_id"]
    event_name = event["data"]["event_name"]
    launch_exploratory_worker(tuning_id, event_name)
