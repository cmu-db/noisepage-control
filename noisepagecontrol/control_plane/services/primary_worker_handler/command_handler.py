from control_plane.services.command_queue.command_types import CommandType

from .capture_primary_workload import capture_primary_workload
from .launch_primary_worker import launch_primary_worker


def handle_command(command):

    command_type = command["command_type"]

    if command_type == CommandType.LAUNCH_PRIMARY_WORKER:
        handle_launch_primary_worker_command(command)
    elif command_type == CommandType.CAPTURE_PRIMARY_WORKLOAD:
        handle_capture_primary_workload_command(command)


def handle_launch_primary_worker_command(command):

    tuning_id = command["data"]["tuning_id"]
    command_name = command["data"]["command_name"]

    """
        Fetch associated tuning instance.
        We need to pass primary port to the launched worker
    """
    from control_plane.services.tuning_manager.models import TuningInstance

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)

    launch_primary_worker(
        tuning_id,
        tuning_instance.primary_port,
        command_name,
    )


def handle_capture_primary_workload_command(command):

    tuning_id = command["data"]["tuning_id"]
    command_name = command["data"]["command_name"]
    capture_primary_workload(tuning_id, command_name)
