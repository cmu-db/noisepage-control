import json

from kombu import Connection, Exchange, Queue

from .config import (
    ampq_exchange,
    ampq_queue,
    ampq_connection_string,
)


def publish_event(event_type, data, completed=False):

    event = {
        "event_type": event_type,
        "data": data,
        "completed": completed,
    }

    with Connection(ampq_connection_string) as connection:
        with connection.Producer(serializer="json") as producer:
            producer.publish(
                json.dumps(event),
                exchange=ampq_exchange,
                routing_key="event",
                declare=[ampq_queue],
            )
