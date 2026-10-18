from .models import Level


class Analyzer:
    '''
    Класс Анализатор

    Собирает статистику, с поступивших в него событий

    Attributes:
        total_events: общее колчиство проанализированных событий

        events_by_level: количество собыйти по уровням

        events_by_source: количество событий по источникам

        top_errors_sources: топ-5 источников ошибок

        first_timestamp: время самого раннего события

        last_timestamp: время самого позднего события
    '''
    def __init__(self):
        '''
        Инициализация атрибутов
        '''
        self.total_events = 0
        self.events_by_level = {}
        self.events_by_source = {}
        self.top_errors_sources = {}
        self.first_timestamp = None
        self.last_timestamp = None


    def add(self, event):
        '''
        Функция накопления статистики

        Args:
            event: событие, с которого собирается статистика
        '''
        self.total_events += 1

        #методом level присваевам строку в переменную level и ищем ключ в словаре для value+=1
        level = event.level
        self.events_by_level[level] = self.events_by_level.get(level, 0) + 1

        source = event.source
        self.events_by_source[source] = self.events_by_source.get(source, 0) + 1

        #сбор топ-n источников error и critical
        if event.level == Level.ERROR or event.level == Level.CRITICAL:
            self.top_errors_sources[source] = self.top_errors_sources.get(source, 0) + 1

        #отбор последнего и первого события
        if self.first_timestamp is None:
            self.first_timestamp = event.timestamp
        if event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp

        if self.last_timestamp is None:
            self.last_timestamp = event.timestamp
        if event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp


    def build(self):
        '''
        Функция получения статистики

        Returns:
            Накопленная статистика
        
        '''
        top_error_sources = sorted(
            self.events_by_source.items(),
            key=lambda item: item[1],
            reverse=True)[:5]

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
