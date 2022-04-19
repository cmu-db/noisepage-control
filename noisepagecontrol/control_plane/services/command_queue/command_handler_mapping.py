from .command_handler_types import CommandHandlerType
from .command_types import CommandType

CommandHandlerMapping = {
    CommandType.LAUNCH_PRIMARY_WORKER: CommandHandlerType.PRIMARY_WORKER_HANDLER,
    CommandType.CAPTURE_PRIMARY_WORKLOAD: CommandHandlerType.PRIMARY_WORKER_HANDLER,
    CommandType.LAUNCH_EXPLORATORY_WORKER: CommandHandlerType.EXPLORATORY_WORKER_HANDLER,
    CommandType.LAUNCH_EXPLORATORY_POSTGRES: CommandHandlerType.EXPLORATORY_WORKER_HANDLER,
    CommandType.STOP_EXPLORATORY_POSTGRES: CommandHandlerType.EXPLORATORY_WORKER_HANDLER,
    CommandType.COLLECT_DATA_FROM_EXPLORATORY: CommandHandlerType.EXPLORATORY_WORKER_HANDLER,
    CommandType.START_TUNING: CommandHandlerType.TUNING_MANAGER,
}
