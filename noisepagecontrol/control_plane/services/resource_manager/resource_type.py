from enum import Enum


class ResourceType(str, Enum):

    WORKLOAD = "WORKLOAD"
    EXPLORATORY_DATA = "EXPLORATORY_DATA"
    TRAINING_DATA = "TRAINING_DATA"
