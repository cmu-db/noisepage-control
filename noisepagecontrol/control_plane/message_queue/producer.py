from kombu import Connection, Exchange, Queue
from control_plane.message_queue.config import (
    message_exchange,
    message_queue,
    ampq_connection_string,
)

def publish_message():
    with Connection(ampq_connection_string) as connection:
        producer = connection.Producer(serializer="json")
        for i in range(10):
            print("Publishing message", i)
            producer.publish(
                {"name": "message " + str(i)},
                exchange=message_exchange,
                routing_key="message",
                declare=[message_queue],
            )
