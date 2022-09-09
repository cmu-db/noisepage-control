from .command_handler_types import CommandHandlerType
from .command_types import CommandType

CommandHandlerMapping = {
    CommandType.REGISTER_DATABASE: CommandHandlerType.REGISTRATION_HANDLER,
    CommandType.LAUNCH_PRIMARY_DAEMON: CommandHandlerType.ENVIRONMENT_HANDLER,
    CommandType.LAUNCH_REPLICA_DAEMON: CommandHandlerType.ENVIRONMENT_HANDLER,
}
