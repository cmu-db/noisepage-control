from kombu import Connection, Exchange, Queue
from control_plane.event_queue.config import (
    ampq_queue,
    ampq_connection_string,
)


def init_message_consumer():
    with Connection(ampq_connection_string) as connection:
        consumer = connection.Consumer(ampq_queue, callbacks=[process_message])
        while True:
            connection.drain_events()


def process_message(body, message):
    print("Message received: ", body)
    message.ack()
