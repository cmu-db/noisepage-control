from kombu import Connection, Exchange, Queue
from control_plane.message_queue.config import (
    message_exchange,
    message_queue,
    ampq_connection_string,
)

def init_message_consumer():
    with Connection(ampq_connection_string) as connection:
        consumer = connection.Consumer(message_queue, callbacks=[process_message])
        while True:
            connection.drain_events()


def process_message(body, message):
    print("Message received: ", body)
    message.ack()
