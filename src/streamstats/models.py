from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


from .errors import InvalidEventError, InvalidTimestampError


@dataclass
class Event:
    timestamp: datetime
    level: Level
    source: str
    message: str

    #обработка пустых полей
    def __post_init__(self):
        if not isinstance(self.timestamp, datetime):
            raise InvalidTimestampError("Invalid timestamp")
        if not isinstance(self.level, Level):
            raise InvalidEventError("No information in level")
        if not isinstance(self.source, str) or not self.source.strip():
            raise InvalidEventError("No information in source")
        if not isinstance(self.message, str):
            raise InvalidEventError("No infromation in message")


class Level(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    #обработка неизвестных уровней
    @classmethod
    def _missing_(cls, value):
        raise InvalidEventError(f"Unknown level: {value!r}")
