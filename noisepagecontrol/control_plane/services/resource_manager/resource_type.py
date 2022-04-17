from enum import Enum


class ResourceType(str, Enum):

    WORKLOAD = "WORKLOAD"
    CATALOG = "CATALOG"
    TRAINING_DATA = "TRAINING_DATA"
