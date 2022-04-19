import logging

from control_plane.services.command_queue.producer import publish_command

logger = logging.getLogger("control_plane")


def publish_child_commands(completed_command):
    """
    This method is only executed on the consumer thread
    No contention, so we don't need any locks
    """

    tuning_id = completed_command["data"]["tuning_id"]
    command_name = completed_command["data"]["command_name"]

    # Single thread runs the consumer
    # We don't have to worry about race against updates
    # Lock free programming hehe

    # Find the tuning command
    # Consumer runs on a seperate thread, started
    # before AppRead => This file gets imported before AppReady
    # But models can be imported only after AppReady
    # Hack to allow "lazy" import of models
    from control_plane.services.tuning_manager.models import TuningCommand

    tuning_command = TuningCommand.objects.get(
        tuning_id=tuning_id, command_name=command_name
    )

    # Duplicate ack for command; ignore
    if tuning_command.completed:
        return

    # Mark current command as True
    tuning_command.completed = True
    tuning_command.save()

    # Find next commands
    for child_command in find_child_commands(tuning_command):

        logger.info("Found child command %s" % (child_command.command_name))

        if can_execute_command(child_command):
            logger.info("Can execute child command %s" % (child_command.command_name))
            publish_command(
                command_type=child_command.command_type,
                data={
                    "tuning_id": tuning_id,
                    "command_name": child_command.command_name,
                    "config": child_command.config,
                },
                completed=False,
            )
        else:
            logger.info(
                "Cannot execute child command %s yet" % (child_command.command_name)
            )


def find_child_commands(tuning_command):

    # Hack to allow "lazy" import of models
    from control_plane.services.tuning_manager.models import TuningCommand

    return TuningCommand.objects.filter(
        tuning_id=tuning_command.tuning_id,
        parent_command_names__contains=[tuning_command.command_name],
    )


def can_execute_command(tuning_command):

    # Hack to allow "lazy" import of models
    from control_plane.services.tuning_manager.models import TuningCommand

    # Get all commands that are required to be completed before
    # potential_next_command can be executed
    parent_command_names = tuning_command.parent_command_names
    parent_commands = list(
        TuningCommand.objects.filter(
            tuning_id=tuning_command.tuning_id, command_name__in=parent_command_names
        )
    )

    # tuning_command can be executed if all parent commands have completed
    return all(map(lambda command: command.completed, parent_commands))
