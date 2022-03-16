from enum import Enum

class EventType(str, Enum):

    LAUNCH_PRIMARY_WORKER = "LAUNCH_PRIMARY_WORKER"
    LAUNCH_EXPLORATORY_WORKER = "LAUNCH_EXPLORATORY_WORKER"
    PRIMARY_WORKER_READY = "PRIMARY_WORKER_READY"
    EXPLORATORY_WORKER_READY = "EXPLORATORY_WORKER_READY"
