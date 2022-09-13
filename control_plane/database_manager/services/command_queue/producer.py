import json

from kombu import Connection

from .config import ampq_connection_string, ampq_exchange, ampq_queue


def publish_command(command_type, command_id, database_id, data, completed=False):

    command = {
        "command_type": command_type,
        "command_id": command_id,
        "database_id": database_id,
        "data": data,
        "completed": completed,
    }

    print("publishing", command)
    with Connection(ampq_connection_string) as connection:
        with connection.Producer(serializer="json") as producer:
            producer.publish(
                json.dumps(command),
                exchange=ampq_exchange,
                routing_key="command",
                declare=[ampq_queue],
            )
