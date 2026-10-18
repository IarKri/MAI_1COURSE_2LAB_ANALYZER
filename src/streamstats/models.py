import argparse
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


from .errors import  CLIConfigError, InvalidEventError, InvalidTimestampError


@dataclass
class Event:
    '''
    Класс событие

    Хранит в себе информацию о событии

    Atributes:
        timestamp: время события

        level: уровень события

        source: источник события

        message: сообщение о событии
    '''
    timestamp: datetime
    level: Level
    source: str
    message: str

    # обработка пустых полей
    def __post_init__(self):
        '''
        Постобработка события на валидность обязательных полей
        '''
        if not isinstance(self.timestamp, datetime):
            raise InvalidTimestampError("Invalid timestamp")
        if not isinstance(self.level, Level):
            raise InvalidEventError("No information in level")
        if not isinstance(self.source, str) or not self.source.strip():
            raise InvalidEventError("No information in source")
        if not isinstance(self.message, str) or not self.message.strip():
            raise InvalidEventError("No infromation in message")


class Level(StrEnum):
    '''
    Класс уровень

    Хранит в себе информацию о допустимых уровнях событий

    Atributes:
        DEBUG: уровень события

        INFO: уровень события

        WARNING: уровень события

        ERROR: уровень события

        CRITICAL: уровень события    
    '''
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    # обработка неизвестных уровней
    @classmethod
    def _missing_(cls, value):
        '''
        Проверка известности уровня события, для ловли кастомной ошибки

        Args:
            cls: данные класса Level

            value: ненайденное значение

        Raises:
            InvalidEventError: Ошибка в анализируемом событии

        '''
        raise InvalidEventError(f"Unknown level: {value!r}")


class CustomArgumentParser(argparse.ArgumentParser):
    '''
    Класс кастомных ошибок для argparser
    '''

    def error(self, message):
        '''
        Замена ошибки argparse на кастомную ошибку

        Args:
            error: информация об ошибке argparse

        Raises:
            CLIConfigError: ошибка аргументов командной строки

        '''
        raise CLIConfigError(message)
