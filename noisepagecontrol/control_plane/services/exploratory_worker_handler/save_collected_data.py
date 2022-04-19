from control_plane.services.command_queue.command_types import CommandType
from control_plane.services.command_queue.producer import publish_command
from control_plane.services.resource_manager.save_resource import save_resource


def save_collected_data(tuning_id, resource_id, data_tar, data_filename, command_name):

    save_resource(tuning_id, resource_id, data_tar, data_filename)

    # Publish COLLECT_DATA_FROM_EXPLORATORY command as completed
    publish_command(
        command_type=CommandType.COLLECT_DATA_FROM_EXPLORATORY,
        data={"tuning_id": tuning_id, "command_name": command_name},
        completed=True,
    )
