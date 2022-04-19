import json

import control_plane.services.exploratory_worker_handler.command_handler as exploratory_worker_command_handler
import control_plane.services.primary_worker_handler.command_handler as primary_worker_command_handler
import control_plane.services.tuning_manager.command_handler as tuning_manager_command_handler
from kombu import Connection

from .child_command_publisher import publish_child_commands
from .config import ampq_connection_string, ampq_queue
from .command_handler_mapping import CommandHandlerMapping
from .command_handler_types import CommandHandlerType

# This maps command_handler_type -> module that handles that command
command_handler = {
    CommandHandlerType.TUNING_MANAGER: tuning_manager_command_handler,
    CommandHandlerType.PRIMARY_WORKER_HANDLER: primary_worker_command_handler,
    CommandHandlerType.EXPLORATORY_WORKER_HANDLER: exploratory_worker_command_handler,
}


def init_command_consumer():
    with Connection(ampq_connection_string) as connection:
        consumer = connection.Consumer(ampq_queue, callbacks=[process_command])
        consumer.consume()
        while True:
            connection.drain_events()


def process_command(command, message_obj):

    command = json.loads(command)
    command_type = command["command_type"]
    command_handler_type = CommandHandlerMapping[command_type]
    completed = command["completed"]

    if completed:
        publish_child_commands(command)
    else:
        command_handler[command_handler_type].handle_command(command)

    message_obj.ack()
