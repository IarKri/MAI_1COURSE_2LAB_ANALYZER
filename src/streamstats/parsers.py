import csv
import json
from datetime import datetime
from pathlib import Path

from .models import Event, Level
from .errors import StreamStatsError, InvalidEventError

#парсер csv файлов
def csv_parser(INPUT):
    path=Path(INPUT)
    with open(path, encoding="utf-8", newline="") as file:
        sample=file.readline()
        file.seek(0)

        separator = csv.Sniffer().sniff(sample,delimiters=",;\t|")

        reader = csv.DictReader(file, dialect=separator)


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
