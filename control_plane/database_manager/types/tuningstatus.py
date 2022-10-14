from enum import Enum


class TuningStatusType(str, Enum):

    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
