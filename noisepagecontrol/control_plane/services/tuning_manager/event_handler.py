from control_plane.services.event_queue.event_types import EventType


def handle_event(event):

    event_type = event["event_type"]

    if event_type == EventType.EXPLORATORY_WORKER_READY:
        handle_exploratory_worker_ready_event(event)
    elif event_type == EventType.PRIMARY_WORKER_READY:
        handle_primary_worker_ready_event(event)


def handle_exploratory_worker_ready_event(event):
    print("Exploratory worker ready event!!")
    pass


def handle_primary_worker_ready_event(event):
    print("Primary worker ready event!!")
    pass
