import json

from kombu import Connection, Exchange, Queue

from .config import (
    ampq_exchange,
    ampq_queue,
    ampq_connection_string,
)

def publish_message(event_type, event_target, data):

    message = {
        "event_type": event_type,
        "event_target": event_target,
        "data": data
    }

    with Connection(ampq_connection_string) as connection:
        with connection.Producer(serializer="json") as producer:
            producer.publish(
                json.dumps(message),
                exchange = ampq_exchange,
                routing_key = "message",
                declare = [ ampq_queue ],
            )
