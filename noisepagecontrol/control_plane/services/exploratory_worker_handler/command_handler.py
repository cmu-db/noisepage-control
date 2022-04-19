import json
import logging

from control_plane.services.command_queue.command_types import CommandType

from .collect_data_from_exploratory import collect_data_from_exploratory
from .launch_exploratory_postgres import launch_exploratory_postgres
from .launch_exploratory_worker import launch_exploratory_worker
from .stop_exploratory_postgres import stop_exploratory_postgres

logger = logging.getLogger("control_plane")


def handle_command(command):
    """
    Input format:
    command = {
        "command_type": CommandType,
        "data": {"tuning_id": str, "command_name": str, "config": dict},
        "completed": bool,
    }
    """
    logger.info(f"Handling command: {json.dumps(command)}")

    command_type = command["command_type"]

    if command_type == CommandType.LAUNCH_EXPLORATORY_WORKER:
        handle_launch_exploratory_worker_command(command)
    elif command_type == CommandType.LAUNCH_EXPLORATORY_POSTGRES:
        handle_launch_exploratory_postgres_command(command)
    elif command_type == CommandType.STOP_EXPLORATORY_POSTGRES:
        handle_stop_exploratory_postgres_command(command)
    elif command_type == CommandType.COLLECT_DATA_FROM_EXPLORATORY:
        handle_collect_data_from_exploratory_command(command)


def handle_launch_exploratory_worker_command(command):

    tuning_id = command["data"]["tuning_id"]
    command_name = command["data"]["command_name"]

    """
        Fetch associated tuning instance.
        We need to pass replica port to the launched worker
    """
    from control_plane.services.tuning_manager.models import TuningInstance

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)

    launch_exploratory_worker(
        tuning_id,
        tuning_instance.replica_port,
        command_name,
    )


def handle_launch_exploratory_postgres_command(command):
    tuning_id = command["data"]["tuning_id"]
    command_name = command["data"]["command_name"]
    config = command["data"]["config"]

    from control_plane.services.tuning_manager.models import TuningInstance

    from .exploratory_pg_status_types import ExploratoryPGStatusType
    from .models import ExploratoryPGInfo

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)
    replica_url = tuning_instance.replica_url

    # Get config.snapshot to decide if exploratory postgres cluster should be
    # launched by taking a snapshot of replica cluster. Default to false.
    snapshot = config["snapshot"] if "snapshot" in config else False

    # Track status for exploratory pg instances
    exploratory_pg_info = ExploratoryPGInfo(
        tuning_id=tuning_id,
        launch_command_name=command_name,
        status=ExploratoryPGStatusType.PENDING,
    )
    exploratory_pg_info.save()

    launch_exploratory_postgres(command_name, replica_url, snapshot)


def handle_stop_exploratory_postgres_command(command):
    tuning_id = command["data"]["tuning_id"]
    config = command["data"]["config"]

    from control_plane.services.tuning_manager.models import TuningInstance

    from .exploratory_pg_status_types import ExploratoryPGStatusType
    from .models import ExploratoryPGInfo

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)
    replica_url = tuning_instance.replica_url

    # We need to get the command name that launches the exploratory PG cluster
    # to know which exploratory port to stop
    if "launch_command" not in config:
        logger.error(
            f"Not specifying launch_command config in {CommandType.STOP_EXPLORATORY_POSTGRES} command"
        )
        return
    launch_command = config["launch_command"]

    info = ExploratoryPGInfo.objects.get(
        tuning_id=tuning_id, launch_command_name=launch_command
    )
    port = info.exploratory_pg_port

    stop_exploratory_postgres(replica_url, port)

    info.status = ExploratoryPGStatusType.STOPPED
    info.save()


def handle_collect_data_from_exploratory_command(command):
    print("Collecting data from exploratory", command)

    tuning_id = command["data"]["tuning_id"]
    command_name = command["data"]["command_name"]

    config = command["data"]["config"]

    target = config["target"]
    data_collector_type = config["data_collector_type"]
    data_collector_config = config["data_collector_config"]

    from control_plane.services.tuning_manager.models import TuningInstance

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)

    """
        If target is replica, execute data collector on production replica
        Else query the exploratory postgres corresponding
            to the provided launch command name
    """
    if target == "replica":
        postgres_port = tuning_instance.replica_port
    else:
        # TODO: query db for exploratory pg port
        postgres_port = "20000"

    collect_data_from_exploratory(
        tuning_id,
        command_name,
        tuning_instance.replica_url,
        postgres_port,
        data_collector_type,
        data_collector_config,
    )
