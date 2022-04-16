from control_plane.services.event_queue.event_types import EventType

from .launch_exploratory_worker import launch_exploratory_worker
from .launch_exploratory_postgres import launch_exploratory_postgres


def handle_event(event):
    """
    Input format:
    event = {
        "event_type": EventType,
        "data": {"tuning_id": str, "event_name": str},
        "completed": bool,
    }
    """

    event_type = event["event_type"]

    if event_type == EventType.LAUNCH_EXPLORATORY_WORKER:
        handle_launch_exploratory_worker_event(event)
    elif event_type == EventType.LAUNCH_EXPLORATORY_POSTGRES:
        handle_launch_exploratory_postgres_event(event)
    elif event_type == EventType.COLLECT_BEHAVIOR_TRAINING_DATA:
        handle_collect_behavior_training_data_event(event)
    elif event_type == EventType.STOP_EXPLORATORY_POSTGRES:
        handle_stop_exploratory_postgres_event(event)


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

    launch_exploratory_postgres(tuning_id, event_name)


def handle_collect_behavior_training_data_event(event):
    pass


def handle_stop_exploratory_postgres_event(event):
    pass
