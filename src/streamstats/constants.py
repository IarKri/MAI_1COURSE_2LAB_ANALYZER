Events_content = ["timestamp", "level", "source", "message"]
Levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
Statistics = {
    "total_events": 0,
    "events_by_level":{
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    },
    "events_by_source": {},
    "top_errors_sources": {},
    "first_timestamp": "",
    "last_timestamp": ""
}