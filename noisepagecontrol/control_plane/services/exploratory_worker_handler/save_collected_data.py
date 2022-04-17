from control_plane.services.event_queue.producer import publish_event
from control_plane.services.event_queue.event_types import EventType


from control_plane.services.resource_manager.save_resource import (
    save_resource,
)


def save_collected_data(tuning_id, resource_id, data_tar, data_filename, event_name):

    save_resource(tuning_id, resource_id, data_tar, data_filename)

    # Publish COLLECT_DATA_FROM_EXPLORATORY event as completed
    publish_event(
        event_type=EventType.COLLECT_DATA_FROM_EXPLORATORY,
        data={"tuning_id": tuning_id, "event_name": event_name},
        completed=True,
    )
