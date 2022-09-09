import json

import database_manager.services.registration_manager.command_handler as registration_command_handler
import database_manager.services.environment_manager.command_handler as environment_command_handler
from kombu import Connection

from .child_command_publisher import publish_child_commands
from .command_handler_mapping import CommandHandlerMapping
from .command_handler_types import CommandHandlerType
from .config import ampq_connection_string, ampq_queue

# This maps command_handler_type -> module that handles that command
command_handler = {
    CommandHandlerType.REGISTRATION_HANDLER: registration_command_handler,
    CommandHandlerType.ENVIRONMENT_HANDLER: environment_command_handler,
}


def init_command_consumer():
    with Connection(ampq_connection_string) as connection:
        consumer = connection.Consumer(ampq_queue, callbacks=[process_command])
        consumer.consume()
        while True:
            connection.drain_events()


def process_command(command, message_obj):

    print ("consumed", command)
    command = json.loads(command)
    command_type = command["command_type"]
    command_handler_type = CommandHandlerMapping[command_type]
    completed = command["completed"]

    if completed:
        publish_child_commands(command)
    else:
        command_handler[command_handler_type].handle_command(command)

    message_obj.ack()
