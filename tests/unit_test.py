import json
import pytest
from pathlib import Path


from streamstats.errors import InvalidEventError, InvalidTimestampError
from streamstats.models import Level
from streamstats.parsers import csv_parser, jsonl_parser


def test_jsonl_parser_valid(tmp_path):
    file = Path(tmp_path/"data_for_valid_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "INFO", "source": "api", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    event = list(jsonl_parser(file, None, 0))

    assert len(event) == 1
    assert event[0].level == Level.INFO
    assert event[0].source == "api"
    assert event[0].message == "Сервис запущен"


def test_csv_parser_valid(tmp_path):
    file = Path(tmp_path/"data_for_valid_tests.csv")

    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-13T11:55:00,INFO,api,Запуск API\n",
        encoding="utf-8"
    )

    event = list(csv_parser(file, None, 0))

    assert len(event) == 1
    assert event[0].level == Level.INFO
    assert event[0].source == "api"
    assert event[0].message == "Запуск API"


def test_jsonl_pasrer_invalid_level(tmp_path):
    file = Path(tmp_path/"data_for_invalid_level_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "IMFO", "source": "api", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    with pytest.raises(InvalidEventError):
        list(jsonl_parser(file, None, 0))


def test_jsonl_parser_invalid_source(tmp_path):
    file = Path(tmp_path/"data_for_invalid_source_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "INFO", "source": "", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    with pytest.raises(InvalidEventError):
        list(jsonl_parser(file, None, 0))


def test_jsonl_parser_invalid_timestamp(tmp_path):
    file = Path(tmp_path/"data_for_invalid_timestamp_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "не время", "level": "INFO", "source": "", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    with pytest.raises(InvalidTimestampError):
        list(jsonl_parser(file, None, 0))


def test_jsonl_parser_invalid_message(tmp_path):
    file = Path(tmp_path/"data_for_invalid_message_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "INFO", "source": "", "message": ""},
                               ensure_ascii=False), encoding="utf-8")

    with pytest.raises(InvalidEventError):
        list(jsonl_parser(file, None, 0))


def test_csv_pasrer_invalid_level(tmp_path):
    file = Path(tmp_path/"data_for_invalid_level_tests.csv")

    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-13T11:55:00,IMFO,api,Запуск API\n",
        encoding="utf -8"
    )

    with pytest.raises(InvalidEventError):
        list(csv_parser(file, None, 0))


def test_csv_parser_invalid_source(tmp_path):
    file = Path(tmp_path/"data_for_invalid_source_tests.csv")

    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-13T11:55:00,INFO,,Запуск API\n",
        encoding="utf -8"
    )

    with pytest.raises(InvalidEventError):
        list(csv_parser(file, None, 0))


def test_csv_parser_invalid_timestamp(tmp_path):
    file = Path(tmp_path/"data_for_invalid_timestamp_tests.csv")

    file.write_text(
        "timestamp,level,source,message\n"
        "234,INFO,api,Запуск API\n",
        encoding="utf -8"
    )

    with pytest.raises(InvalidTimestampError):
        list(csv_parser(file, None, 0))


def test_csv_parser_invalid_message(tmp_path):
    file = Path(tmp_path/"data_for_invalid_message_tests.csv")

    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-13T11:55:00,INFO,api,\n",
        encoding="utf -8"
    )

    with pytest.raises(InvalidEventError):
        list(csv_parser(file, None, 0))


def test_jsonl_parser_skip_invalid():
    file = Path("tests_invalid_data/data_for_parser_skip_invalid_test.jsonl")

    event = list(jsonl_parser(file, 1, 1))
    assert len(event) == 0


def test_csv_parser_skip_invalid():
    file = Path("tests_invalid_data/data_for_parser_skip_invalid_test.csv")

    event = list(csv_parser(file, 1, 1))
    assert len(event) == 0


def test_jsonl_unicode():
    file = Path("tests_valid_data/data_for_unicode_test.jsonl")

    event = list(jsonl_parser(file, None, 0))

    assert len(event) == 2
    assert event[0].source == "服务器"
    assert event[1].source == 'сервер'


def test_csv_unicode():
    file = Path("tests_valid_data/data_for_unicode_test.csv")

    event = list(csv_parser(file, None, 0))

    assert len(event) == 2
    assert event[0].source == "服务器"
    assert event[1].source == 'сервер'
