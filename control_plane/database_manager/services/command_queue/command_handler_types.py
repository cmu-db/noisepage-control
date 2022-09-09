from enum import Enum


class CommandHandlerType(str, Enum):

    REGISTRATION_HANDLER = "REGISTRATION_HANDLER"
    ENVIRONMENT_HANDLER = "ENVIRONMENT_HANDLER"
