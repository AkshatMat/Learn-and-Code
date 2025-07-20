from enum import Enum, auto

class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

    def __str__(self):
        return self.name

def get_level_from_string(level_str):
    try:
        return LogLevel[level_str.upper()]
    except KeyError:
        valid_levels = ', '.join([level.name for level in LogLevel])
        raise ValueError(f"Invalid log level: {level_str}. Valid levels are: {valid_levels}")