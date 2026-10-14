from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


@dataclass
class Event:
    timestamp: datetime
    level: Level
    source: str
    message: str

class Level(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
