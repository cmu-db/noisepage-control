from enum import Enum


class ResourceType(str, Enum):

    KEY = "KEY"
    WORKLOAD = "WORKLOAD"
    STATE = "STATE"
