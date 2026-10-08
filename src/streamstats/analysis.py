from .models import Level

class Analyzer:
    def __init__(self):
        total_events = 0
        events_by_level = {}
        events_by_source = {}
        top_errors_sources = {}
        first_timestamp = None
        last_timestamp = None

    def add(self, event):
        self.total_events += 1

        level = event.level
        self.events_by_level[level] = self.events_by_level.get(level, 0) + 1

        source = event.source
        self.events_by_source[source] = self.events_by_source.get(source, 0) + 1

        if event.level == Level.ERROR or event.level == Level.CRITICAL:
            self.top_error_sources[source] = (self.top_error_sources.get(source, 0) + 1)

        if self.first_timestamp is None:
            self.first_timestamp = event.timestamp
        elif event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp

        if self.last_timestamp is None:
            self.last_timestamp = event.timestamp
        elif event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp