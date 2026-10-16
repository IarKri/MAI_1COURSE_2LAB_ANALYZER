from datetime import datetime
import logging

from .errors import StreamStatsError
from .models import Level



class Analyzer:

    #метод для инициализации содержимого
    def __init__(self):
        self.total_events = 0
        self.events_by_level = {}
        self.events_by_source = {}
        self.top_errors_sources = {}
        self.first_timestamp = None
        self.last_timestamp = None




        logger=logging.getLogger(__name__)




        

    #метод обработки событий
    def add(self, event):
        self.total_events += 1

        #методом level присваевам строку в переменную level и ищем ключ в словаре для увеличения значения
        level = event.level
        self.events_by_level[level] = self.events_by_level.get(level, 0) + 1

        source = event.source
        self.events_by_source[source] = self.events_by_source.get(source, 0) + 1

        #сбор топ-n источников error и critical
        if event.level == Level.ERROR or event.level == Level.CRITICAL:
            self.top_errors_sources[source] = (self.top_errors_sources.get(source, 0) + 1)

        #отбор последнего и первого события
        if self.first_timestamp is None:
            self.first_timestamp = event.timestamp
        if event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp

        if self.last_timestamp is None:
            self.last_timestamp = event.timestamp
        if event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp

    def add_skip_invalid(self, event, counter):
        skipped_lines = 0
        self.total_events += 1

        level = event.level
        source = event.source
        try:
            self.events_by_level[level] = self.events_by_level.get(level, 0) + 1
        except Exception as error:
            print (f"file: {counter+2}, line: {self.total_events}, WARNING: {error}")
        try:
            self.events_by_source[source] = self.events_by_level.get(source, 0) + 1
        except StreamStatsError as error:
            print (f"file: {counter+2}, line: {self.total_events}, WARNING: {error}")



        #дописать при необходимости

        if event.level == Level.ERROR or event.level == Level.CRITICAL:
            self.top_errors_sources[source] = (self.top_errors_sources.get(source, 0) + 1)

        #отбор последнего и первого события
        if self.first_timestamp is None:
            self.first_timestamp = event.timestamp
        if event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp

        if self.last_timestamp is None:
            self.last_timestamp = event.timestamp
        if event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp




    #метод вывода итоговой статистики
    def build(self):
        top_error_sources = sorted(
            self.events_by_source.items(),
            key=lambda item: item[1],
            reverse=True)[:5]               #удобно менять количество вывода

        top_error_sources = dict(top_error_sources)

        return {
            "total_events": self.total_events,
            "events_by_level": self.events_by_level,
            "events_by_source": self.events_by_source,
            "top_error_sources": top_error_sources,
            "first_timestamp": 
                self.first_timestamp.isoformat(),
            "last_timestamp":
                self.last_timestamp.isoformat(),
        }