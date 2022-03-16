import json
from kombu import Connection, Exchange, Queue

from .config import (
    ampq_queue,
    ampq_connection_string,
)
from .event_handler_types import EventHandlerType
from .event_types import EventType

import control_plane.services.primary_worker_handler.event_handler as primary_worker_event_handler
import control_plane.services.exploratory_worker_handler.event_handler as exploratory_worker_event_handler

# This maps event_handler_type -> module that handles that event
event_handler = {
    EventHandlerType.PRIMARY_WORKER_HANDLER: primary_worker_event_handler,
    EventHandlerType.EXPLORATORY_WORKER_HANDLER: exploratory_worker_event_handler,
}


def init_event_consumer():
    with Connection(ampq_connection_string) as connection:
        consumer = connection.Consumer(ampq_queue, callbacks=[process_event])
        consumer.consume()
        while True:
            connection.drain_events()


def process_event(event, message_obj):

    event = json.loads(event)
    event_handler_type = event["event_handler"]
    event_handler[event_handler_type].handle_event(event)
    message_obj.ack()
