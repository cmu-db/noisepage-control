from enum import Enum


class DatabaseStateType(str, Enum):

    REGISTERING = "REGISTERING"  # Do not permit actions

    """
    Only permit actions (collect workload, metrics, etc. if state is currently HEALTHY)
    """
    HEALTHY = "HEALTHY"  # Permit actions
    UNHEALTHY = "UNHEALTHY"  # Do not permit actions

    """
    Allow only one action at a time;
    If ain any one of these states, do not allow other actions
    """
    TUNING = "TUNING"
    COLLECTING_WORKLOAD = "COLLECTING_WORKLOAD"
    COLLECTING_METRICS = "COLLECTING_METRICS"
    COLLECTING_STATE = "COLLECTING_STATE"
