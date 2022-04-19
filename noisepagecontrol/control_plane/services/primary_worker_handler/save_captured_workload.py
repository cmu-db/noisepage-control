from control_plane.services.command_queue.command_types import CommandType
from control_plane.services.command_queue.producer import publish_command
from control_plane.services.resource_manager.save_resource import save_resource


def save_captured_workload(
    tuning_id, resource_id, workload_tar, workload_filename, command_name
):

    save_resource(tuning_id, resource_id, workload_tar, workload_filename)

    # Publish LAUNCH_PRIMARY_WORKER command as completed
    publish_command(
        command_type=CommandType.CAPTURE_PRIMARY_WORKLOAD,
        data={"tuning_id": tuning_id, "command_name": command_name},
        completed=True,
    )
