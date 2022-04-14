from enum import Enum


class ResourceType(str, Enum):

    WORKLOAD = "WORKLOAD"
    TRAINING_DATA = "TRAINING_DATA"
