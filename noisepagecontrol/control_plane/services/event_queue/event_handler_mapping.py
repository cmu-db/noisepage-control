from .event_handler_types import EventHandlerType
from .event_types import EventType

EventHandlerMapping = {
    EventType.LAUNCH_PRIMARY_WORKER: EventHandlerType.PRIMARY_WORKER_HANDLER,
    EventType.CAPTURE_PRIMARY_WORKLOAD: EventHandlerType.PRIMARY_WORKER_HANDLER,
    EventType.LAUNCH_EXPLORATORY_WORKER: EventHandlerType.EXPLORATORY_WORKER_HANDLER,
    EventType.LAUNCH_EXPLORATORY_POSTGRES: EventHandlerType.EXPLORATORY_WORKER_HANDLER,
    EventType.STOP_EXPLORATORY_POSTGRES: EventHandlerType.EXPLORATORY_WORKER_HANDLER,
    EventType.START_TUNING: EventHandlerType.TUNING_MANAGER,
}
