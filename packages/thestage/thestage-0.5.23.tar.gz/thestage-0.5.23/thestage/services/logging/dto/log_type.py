from enum import Enum


class LogType(str, Enum):
    STDOUT = "STDOUT",
    STDERR = "STDERR"
    PLATFORM_STDOUT = "PLATFORM_STDOUT"
    PLATFORM_STDERR = "PLATFORM_STDERR"
