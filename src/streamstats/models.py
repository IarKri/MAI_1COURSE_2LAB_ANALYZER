from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    timestamp: datetime
    level: Level
    source: str
    message: str

class Level:
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
