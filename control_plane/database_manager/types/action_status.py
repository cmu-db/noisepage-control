from enum import Enum


class ActionStatusType(str, Enum):

    NOT_APPLIED = "NOT_APPLIED"
    APPLYING = "APPLYING"
    APPLIED = "APPLIED"
    FAILED = "FAILED"
