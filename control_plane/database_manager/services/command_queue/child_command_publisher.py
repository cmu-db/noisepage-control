import logging

from .producer import publish_command

logger = logging.getLogger("control_plane")


def publish_child_commands(completed_command):
    """
    This method is only executed on the consumer thread
    No contention, so we don't need any locks
    """

    database_id = completed_command["database_id"]
    command_id = completed_command["command_id"]

    # Single thread runs the consumer
    # We don't have to worry about race against updates
    # Lock free programming hehe

    # Find the tuning command
    # Consumer runs on a seperate thread, started
    # before AppRead => This file gets imported before AppReady
    # But models can be imported only after AppReady
    # Hack to allow "lazy" import of models
    from .models import Command

    command = Command.objects.get(command_id=command_id)

    # Duplicate ack for command; ignore
    if command.completed:
        return

    # Mark current command as True
    command.completed = True
    command.save()

    # Find next commands
    for child_command in find_child_commands(command):

        logger.info("Found child command %s" % (child_command.command_id))

        if can_execute_command(child_command):
            logger.info("Can execute child command %s" % (child_command.command_id))
            publish_command(
                command_type=child_command.command_type,
                command_id = child_command.command_id,
                database_id = database_id,
                data={
                    "command_id": child_command.command_id,
                    "config": child_command.config,
                },
                completed=False,
            )
        else:
            logger.info(
                "Cannot execute child command %s yet" % (child_command.command_id)
            )


def find_child_commands(curr_command):

    # Hack to allow "lazy" import of models
    from .models import Command

    return Command.objects.filter(
        database_id=curr_command.database_id,
        parent_command_ids__contains=[curr_command.command_id],
    )


def can_execute_command(curr_command):

    # Hack to allow "lazy" import of models
    from .models import Command

    # Get all commands that are required to be completed before
    # potential_next_command can be executed
    parent_command_ids = curr_command.parent_command_ids
    parent_commands = list(
        Command.objects.filter(
            database_id=curr_command.database_id, command_id__in=parent_command_ids
        )
    )

    # curr_command can be executed if all parent commands have completed
    return all(map(lambda command: command.completed, parent_commands))
