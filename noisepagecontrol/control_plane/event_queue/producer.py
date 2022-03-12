from kombu import Connection, Exchange, Queue
from control_plane.event_queue.config import (
    ampq_exchange,
    ampq_queue,
    ampq_connection_string,
)


def publish_message():
    with Connection(ampq_connection_string) as connection:
        producer = connection.Producer(serializer="json")
        for i in range(10):
            print("Publishing message", i)
            producer.publish(
                {"name": "message " + str(i)},
                exchange=ampq_exchange,
                routing_key="message",
                declare=[ampq_queue],
            )
