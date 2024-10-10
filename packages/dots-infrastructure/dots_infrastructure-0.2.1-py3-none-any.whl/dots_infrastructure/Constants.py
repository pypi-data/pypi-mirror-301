from enum import Enum

class Command:
    TERMINATE = "0"

class TimeRequestType(Enum):
    PERIOD = 0
    ON_INPUT = 1