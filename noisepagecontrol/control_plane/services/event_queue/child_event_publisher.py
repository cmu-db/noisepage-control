import time
import logging

from control_plane.services.event_queue.event_types import EventType
from control_plane.services.event_queue.event_handler_types import EventHandlerType
from control_plane.services.event_queue.event_handler_mapping import EventHandlerMapping
from control_plane.services.event_queue.producer import publish_event

logger = logging.getLogger("control_plane")


def publish_child_events(completed_event):
    """
    This method is only executed on the consumer thread
    No contention, so we don't need any locks
    """

    tuning_id = completed_event["data"]["tuning_id"]
    event_name = completed_event["data"]["event_name"]

    # Single thread runs the consumer
    # We don't have to worry about race against updates
    # Lock free programming hehe

    # Find the tuning event
    # Consumer runs on a seperate thread, started
    # before AppRead => This file gets imported before AppReady
    # But models can be imported only after AppReady
    # Hack to allow "lazy" import of models
    from control_plane.services.tuning_manager.models import TuningEvent

    tuning_event = TuningEvent.objects.get(tuning_id=tuning_id, event_name=event_name)

    # Duplicate ack for event; ignore
    if tuning_event.completed == True:
        return

    # Mark current event as True
    tuning_event.completed = True
    tuning_event.save()

    # Find next events
    for child_event in find_child_events(tuning_event):

        logger.info("Found child event %s" % (child_event.event_name))

        if can_execute_event(child_event):
            logger.info("Can execute child event %s" % (child_event.event_name))
            publish_event(
                event_type=child_event.event_type,
                data={"tuning_id": tuning_id, "event_name": child_event.event_name, "config": child_event.config},
                completed=False,
            )
        else:
            logger.info("Cannot execute child event %s yet" % (child_event.event_name))


def find_child_events(tuning_event):

    # Hack to allow "lazy" import of models
    from control_plane.services.tuning_manager.models import TuningEvent

    return TuningEvent.objects.filter(
        tuning_id=tuning_event.tuning_id,
        parent_event_names__contains=[tuning_event.event_name],
    )


def can_execute_event(tuning_event):

    # Hack to allow "lazy" import of models
    from control_plane.services.tuning_manager.models import TuningEvent

    # Get all events that are required to be completed before
    # potential_next_event can be executed
    parent_event_names = tuning_event.parent_event_names
    parent_events = list(
        TuningEvent.objects.filter(
            tuning_id=tuning_event.tuning_id, event_name__in=parent_event_names
        )
    )

    # tuning_event can be executed if all parent events have completed
    return all(map(lambda event: event.completed, parent_events))
