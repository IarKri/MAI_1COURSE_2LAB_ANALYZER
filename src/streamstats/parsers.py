import csv
import json
from datetime import datetime
from pathlib import Path

from .models import Event, Level


def csv_parser(INPUT):
    path=Path(INPUT)
    with open(path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)


    #row будет являться словарем
    #присваеваем значения объекту класса через ключи словаря
        for row in reader:
            event = Event(
                timestamp=datetime.fromisoformat(row["timestamp"]),
                level=Level(row["level"]),
                source=row["source"],
                message=row["message"]
            )

        #yield позволить анализировать файлы через event построково \
        # ( выбрасывая промежуточное значение)
            yield event


def json_parser(INPUT):
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
