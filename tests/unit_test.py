from pathlib import Path


from streamstats.models import Level
from streamstats.parsers import csv_parser, jsonl_parser




def test_jsonl_parser():
    file = Path("tests_data/data_for_tests.jsonl")

    #делаем list, потому что через for event in csv_parser(file) потребуется .add (а тест только для парсера)
    event = list(jsonl_parser(file))

    assert len(event) == 1
    assert event[0].level == Level.INFO
    assert event[0].source == "api"
    assert event[0].message == "Сервис запущен"

def test_csv_parser():
    file = Path("tests_data/data_for_tests.csv")
    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-13T11:55:00,INFO,api,Запуск API\n",
        encoding = "utf-8"
    )

    event = list(csv_parser(file))

    assert len(event) == 1
    assert event[0].level == Level.INFO
    assert event[0].source == "api"
    assert event[0].message== "Запуск API"