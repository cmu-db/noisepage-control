from control_plane.services.event_queue.event_types import EventType

from .views import launch_primary_worker

def handle_event(event):
    
    event_type = event["event_type"]

    if event_type == EventType.LAUNCH_PRIMARY_WORKER:
        handle_launch_primary_worker_event(event)


def handle_launch_primary_worker_event(event):

    tuning_uuid = event["data"]["tuning_uuid"]
    launch_primary_worker(tuning_uuid)
