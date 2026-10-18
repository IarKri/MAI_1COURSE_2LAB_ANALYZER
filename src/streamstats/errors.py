class StreamStatsError(Exception):
    '''
    Родительский класс ошибок
    '''
    pass


class UnsupportedFormatError(StreamStatsError):
    """
    Класс ошибки неподдерживаемого формата файла

    Наследуется от SreamStatsError
    """
    pass


class InvalidEventError(StreamStatsError):
    '''
    Класс ошибки неверного события


    Наследуется от StreamStatsError
    '''
    pass


class InvalidTimestampError(StreamStatsError):
    '''
    Класс ошибки неверного timestamp

    Наследуется от StreamStatsError
    '''
    pass


class CLIConfigError(StreamStatsError):
    '''
    Класс ошибки конфигурации CLI


    Наследуется от StreamStatsError
    '''
    pass


class InvalidDelimiterError(StreamStatsError):
    '''
    Класс ошибки неверного раздлителя


    Наследуется от StreamStatsError
    '''
    pass


class UnmatchedFormatsError(StreamStatsError):
    '''
    Класс ошибки несопоставления формата файла и аргумента команды --format

    Наследуется от StreamStatsError
    '''
    pass
