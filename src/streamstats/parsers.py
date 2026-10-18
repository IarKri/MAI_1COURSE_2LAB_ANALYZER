import csv
import json
import logging
from datetime import datetime
from pathlib import Path


from .errors import (
    InvalidDelimiterError,
    InvalidEventError,
    InvalidTimestampError,
)
from .models import Event, Level


logger = logging.getLogger("streamstats")

# logger для обработки ошибок через --skip-invalid


def log_invalid(file_counter, line_counter, error):
    '''
    Логгирование предупреждений об ошибках

    Args:
        file_counter: номер файла с ошибкой

        line_counter: номер строки с ошибкой

        error: Ошибка
    '''
    logger.warning(
        "file %d, line %d, %s, %s",
        file_counter,
        line_counter,
        type(error).__name__,
        error,
    )


# парсер csv файлов
def csv_parser(INPUT, file_counter, skip_invalid):
    '''
    Посторчно читает csv файл и формирует event для analyzer

    Args:
        INPUT: Файлы, подающиеся для анализа на вход

        file_counter: аргумент для логера, показывающий номер файла WARNING-а

        skip_invalid: флаг, по которому определятся пропуск/ловля ошибок

    Yields:
        event: отформатированное событие для analyzer
    '''
    path = Path(INPUT)
    with open(path, encoding="utf-8", newline="") as file:

        # для определения разделителя
        sample = file.readline()

        # для обработки пустого файла
        if not sample:
            return

        file.seek(0)

        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            reader = csv.DictReader(file, dialect=delimiter)

        except csv.Error as error:
            raise InvalidDelimiterError(f"Unsupported delimiter: {error}")

        line_counter = 1

        for row in reader:
            line_counter += 1

            if not skip_invalid:
                if None in row:
                    raise InvalidEventError("Extra colomns")

                try:
                    timestamp = datetime.fromisoformat(row["timestamp"])

                except ValueError:
                    raise InvalidTimestampError(
                        f"Invalid Timestamp: {row["timestamp"]}")

                try:
                    event = Event(
                        timestamp=timestamp,
                        level=Level(row["level"]),
                        source=row["source"],
                        message=row["message"]
                    )

                except ValueError as error:
                    raise InvalidEventError(f"Invalid Event: {error}")

                except KeyError as error:
                    raise InvalidEventError(f"Absence of {error}")

                yield event

            else:
                if None in row:
                    error = InvalidEventError("Extra colomns")
                    log_invalid(file_counter, line_counter, error)
                    continue
                try:
                    timestamp = datetime.fromisoformat(row["timestamp"])

                except ValueError as error:
                    log_invalid(file_counter, line_counter,
                                InvalidTimestampError(f"{error}"))
                    continue

                try:
                    event = Event(
                        timestamp=timestamp,
                        level=Level(row["level"]),
                        source=row["source"],
                        message=row["message"]
                    )

                except (ValueError, KeyError, TypeError, InvalidEventError, InvalidTimestampError) as error:
                    log_invalid(file_counter, line_counter, error)
                    continue

        # yield позволит анализировать файлы через event построково \
        # ( выбрасывая промежуточное значение)
                yield event

# парсер jsonl файлов


def jsonl_parser(INPUT, file_counter, skip_invalid):
    '''
    Посторчно читает jsonl файл и формирует event для analyzer

    Args:
        INPUT: Файлы, подающиеся для анализа на вход

    Yields:
        event: отформатированное событие для analyzer
    '''
    path = Path(INPUT)
    with open(path, encoding="utf-8") as file:
        line_counter = 0

        for line in file:
            line_counter += 1

            if line.strip() == "":
                continue

            if not skip_invalid:
                try:
                    row = json.loads(line)

                except json.JSONDecodeError as error:
                    raise InvalidEventError(f"Invalid event: {error}")

                try:
                    timestamp = datetime.fromisoformat(row["timestamp"])

                except ValueError:
                    raise InvalidTimestampError(
                        f"Invalid Timestamp: {row["timestamp"]}")

                try:
                    event = Event(
                        timestamp=timestamp,
                        level=Level(row["level"]),
                        source=row["source"],
                        message=row["message"]
                    )

                except ValueError as error:
                    raise InvalidEventError(f"Invalid Event: {error}")

                except KeyError as error:
                    raise InvalidEventError(f"Absence of {error}")

                yield event

            else:
                try:
                    row = json.loads(line)

                except json.JSONDecodeError as error:
                    log_invalid(file_counter, line_counter,
                                InvalidEventError(f"Not jsonl format line"))
                    continue
                try:
                    timestamp = datetime.fromisoformat(row["timestamp"])

                except ValueError as error:
                    log_invalid(file_counter,  line_counter,
                                InvalidTimestampError(f"{error}"))
                    continue

                except KeyError as error:
                    log_invalid(file_counter, line_counter,
                                InvalidTimestampError(f"Absence of {error}"))
                    continue

                try:
                    event = Event(
                        timestamp=timestamp,
                        level=Level(row["level"]),
                        source=row["source"],
                        message=row["message"]
                    )

                except ValueError as error:
                    log_invalid(file_counter,  line_counter,
                                InvalidEventError(f"Invalid{error}"))
                    continue

                except KeyError as error:
                    log_invalid(file_counter, line_counter,
                                InvalidEventError(f"Absence of{error}"))
                    continue

                except InvalidEventError as error:
                    log_invalid(file_counter, line_counter,
                                InvalidEventError(f"{error}"))
                    continue

                yield event
