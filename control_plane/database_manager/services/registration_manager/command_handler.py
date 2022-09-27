import json
import logging

logger = logging.getLogger("control_plane")

from database_manager.services.command_queue.command_types import CommandType
from database_manager.services.command_queue.producer import publish_command
from database_manager.database_state_types import DatabaseStateType

from environments.environment import init_environment
from environments.environment_types import EnvironmentType
from environments.self_managed_postgres import SelfManagedPostgresEnvironment
from environments.aws_rds_postgres import AWSRDSPostgresEnvironment

def handle_command(command):
    logger.info(f"Handling command: {json.dumps(command)}")

    command_type = command["command_type"]

    if command_type == CommandType.REGISTER_DATABASE:
        handle_register_database_command(command)
    else:
        print ("No handler found")


def handle_register_database_command(command):

    from database_manager.services.command_queue.models import Command
    from database_manager.models import Database

    command_id = command["command_id"]
    database_id = command["database_id"]

    database = Database.objects.get(database_id = database_id)
    
    # Create approproate environemnt implementation
    env = init_environment(database)
    config_valid, err = env.test_connectivity()

    if not config_valid:
        logger.warning(f'test_connectivity failed. err: {err}')
        database.errors.append(err)
        database.state = DatabaseStateType.UNHEALTHY
    else:
        configured_successfully, err = env.configure()
        
        if not configured_successfully:
            database.errors.append(err)
            database.state = DatabaseStateType.UNHEALTHY

        else:
            database.state = DatabaseStateType.HEALTHY
    database.save()

    publish_command(
        command_type = command["command_type"],
        command_id = command_id,
        database_id = database_id,
        data={},
        completed=True,
    )
