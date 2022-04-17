import json
import logging

from control_plane.services.event_queue.event_types import EventType
from .launch_exploratory_worker import launch_exploratory_worker
from .launch_exploratory_postgres import launch_exploratory_postgres
from .stop_exploratory_postgres import stop_exploratory_postgres
from .collect_data_from_exploratory import collect_data_from_exploratory

logger = logging.getLogger("control_plane")


def handle_event(event):
    """
    Input format:
    event = {
        "event_type": EventType,
        "data": {"tuning_id": str, "event_name": str, "config": dict},
        "completed": bool,
    }
    """
    logger.info(f"Handling event: {json.dumps(event)}")

    event_type = event["event_type"]

    if event_type == EventType.LAUNCH_EXPLORATORY_WORKER:
        handle_launch_exploratory_worker_event(event)
    elif event_type == EventType.LAUNCH_EXPLORATORY_POSTGRES:
        handle_launch_exploratory_postgres_event(event)
    elif event_type == EventType.STOP_EXPLORATORY_POSTGRES:
        handle_stop_exploratory_postgres_event(event)
    elif event_type == EventType.COLLECT_DATA_FROM_EXPLORATORY:
        handle_collect_data_from_exploratory_event(event)


def handle_launch_exploratory_worker_event(event):

    tuning_id = event["data"]["tuning_id"]
    event_name = event["data"]["event_name"]

    """
        Fetch associated tuning instance. 
        We need to pass replica port to the launched worker
    """
    from control_plane.services.tuning_manager.models import TuningInstance

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)

    launch_exploratory_worker(
        tuning_id,
        tuning_instance.replica_port,
        tuning_instance.replica_username,
        event_name,
    )


def handle_launch_exploratory_postgres_event(event):
    tuning_id = event["data"]["tuning_id"]
    event_name = event["data"]["event_name"]
    config = event["data"]["config"]

    from .models import ExploratoryPGInfo
    from .exploratory_pg_status_types import ExploratoryPGStatusType
    from control_plane.services.tuning_manager.models import TuningInstance

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)
    replica_url = tuning_instance.replica_url

    # Get config.snapshot to decide if exploratory postgres cluster should be
    # launched by taking a snapshot of replica cluster. Default to false.
    snapshot = config["snapshot"] if "snapshot" in config else False

    # Track status for exploratory pg instances
    exploratory_pg_info = ExploratoryPGInfo(
        tuning_id=tuning_id,
        launch_event_name=event_name,
        status=ExploratoryPGStatusType.PENDING,
    )
    exploratory_pg_info.save()

    launch_exploratory_postgres(event_name, replica_url, snapshot)


def handle_stop_exploratory_postgres_event(event):
    tuning_id = event["data"]["tuning_id"]
    config = event["data"]["config"]

    from control_plane.services.tuning_manager.models import TuningInstance
    from .models import ExploratoryPGInfo
    from .exploratory_pg_status_types import ExploratoryPGStatusType

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)
    replica_url = tuning_instance.replica_url

    # We need to get the event name that launches the exploratory PG cluster
    # to know which exploratory port to stop
    if "launch_event" not in config:
        logger.error(
            f"Not specifying launch_event config in {EventType.STOP_EXPLORATORY_POSTGRES} event"
        )
        return
    launch_event = config["launch_event"]

    info = ExploratoryPGInfo.objects.get(
        tuning_id=tuning_id, launch_event_name=launch_event
    )
    port = info.exploratory_pg_port

    stop_exploratory_postgres(replica_url, port)

    info.status = ExploratoryPGStatusType.STOPPED
    info.save()


def handle_collect_data_from_exploratory_event(event):
    print("Collecting data from exploratory", event)

    tuning_id = event["data"]["tuning_id"]
    event_name = event["data"]["event_name"]

    config = event["data"]["config"]
    data_collector_type = config["data_collector_type"]
    data_collector_config = config["data_collector_config"]

    from control_plane.services.tuning_manager.models import TuningInstance

    tuning_instance = TuningInstance.objects.get(tuning_id=tuning_id)

    # TODO: This should change based on the data collector type;
    postgres_port = tuning_instance.replica_port

    collect_data_from_exploratory(
        tuning_id,
        event_name,
        tuning_instance.replica_url,
        postgres_port,
        data_collector_type,
        data_collector_config,
    )
