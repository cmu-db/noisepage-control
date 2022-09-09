from enum import Enum


class EnvironmentType(str, Enum):

    SELF_MANAGED_POSTGRES = "SELF_MANAGED_POSTGRES"
    AWS_RDS_POSTGRES = "AWS_RDS_POSTGRES"


