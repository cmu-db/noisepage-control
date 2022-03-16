import json

from kombu import Connection, Exchange, Queue

from .config import (
    ampq_exchange,
    ampq_queue,
    ampq_connection_string,
)


def publish_event(event_type, event_handler, data):

    event = {"event_type": event_type, "event_handler": event_handler, "data": data}

    with Connection(ampq_connection_string) as connection:
        with connection.Producer(serializer="json") as producer:
            producer.publish(
                json.dumps(event),
                exchange=ampq_exchange,
                routing_key="event",
                declare=[ampq_queue],
            )
