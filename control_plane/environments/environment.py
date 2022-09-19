
from .environment_types import EnvironmentType
from .self_managed_postgres import SelfManagedPostgresEnvironment
from .aws_rds_postgres import AWSRDSPostgresEnvironment

def init_environment(database):

    # Create approproate environemnt implementation
    if database.environment_type == EnvironmentType.SELF_MANAGED_POSTGRES:
        env = SelfManagedPostgresEnvironment(database)
    elif database.environment_type == EnvironmentType.AWS_RDS_POSTGRES:
        env = AWSRDSPostgresEnvironment(database)

    return env