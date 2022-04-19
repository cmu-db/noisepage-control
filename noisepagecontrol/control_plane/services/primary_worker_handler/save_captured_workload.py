from control_plane.services.event_queue.event_types import EventType
from control_plane.services.event_queue.producer import publish_event
from control_plane.services.resource_manager.save_resource import save_resource


def save_captured_workload(
    tuning_id, resource_id, workload_tar, workload_filename, event_name
):

    save_resource(tuning_id, resource_id, workload_tar, workload_filename)

    # Publish LAUNCH_PRIMARY_WORKER event as completed
    publish_event(
        event_type=EventType.CAPTURE_PRIMARY_WORKLOAD,
        data={"tuning_id": tuning_id, "event_name": event_name},
        completed=True,
    )
