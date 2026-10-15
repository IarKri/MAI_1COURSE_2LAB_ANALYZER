import csv
import json
from datetime import datetime
from pathlib import Path


from .errors import (
    StreamStatsError,
    InvalidEventError,
    InvalidDelimiterError,
)
from .models import Event, Level

#парсер csv файлов
def csv_parser(INPUT):
    '''
    Посторчно читает csv файл и формирует event для analyzer

    Args:
        INPUT: Файлы, подающиеся для анализа на вход

    Yields:
        event: отформатированное событие для analyzer
    '''
    path=Path(INPUT)
    with open(path, encoding="utf-8", newline="") as file:
        sample=file.readline()
        file.seek(0)

        try:
            delimiter = csv.Sniffer().sniff(sample,delimiters=",;\t|")
            reader = csv.DictReader(file, dialect=delimiter)
        except csv.Error as error:
            raise InvalidDelimiterError("Unsupported delimiter") from error

    #row будет являться словарем
    #присваеваем значения объекту класса через ключи словаря
        for row in reader:
            event = Event(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                level=Level(row["level"]),
                source=row["source"],
                message=row["message"]
                )
 #           except (ValueError, TypeError, KeyError) as error:
 #               raise InvalidEventError(f"{error}: content of event is unsupported") from error

        #yield позволить анализировать файлы через event построково \
        # ( выбрасывая промежуточное значение)
            yield event

#парсер jsonl файлов
def jsonl_parser(INPUT):
    '''
    Посторчно читает jsonl файл и формирует event для analyzer

    Args:
        INPUT: Файлы, подающиеся для анализа на вход

    Yields:
        event: отформатированное событие для analyzer
    '''
    path = Path(INPUT)
    with open(path, encoding="utf-8") as file:
        for line in file:

            if line.strip()=="":
                continue

            row = json.loads(line)
            event = Event(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                level=Level(row["level"]),
                source=row["source"],
                message=row["message"]
            )

            yield event
