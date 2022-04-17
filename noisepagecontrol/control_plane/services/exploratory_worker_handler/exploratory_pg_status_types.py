from enum import Enum


class ExploratoryPGStatusType(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    STOPPED = "STOPPED"
