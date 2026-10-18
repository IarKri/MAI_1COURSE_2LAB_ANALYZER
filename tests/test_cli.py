import json
import pytest
from pathlib import Path


from streamstats.__main__ import main
from streamstats.errors import InvalidEventError, CLIConfigError


def test_valid_cli_csv_no_output(capsys, tmp_path):

    file = Path(tmp_path/"data_for_valid_tests.csv")

    file.write_text("timestamp,level,source,message\n"
                    "2026-10-13T11:55:00,INFO,api,Запуск API\n",
                    encoding="utf-8")

    main(["analyze", str(file), "--format", "csv"])
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "total_events": 1,
        "events_by_level": {
            "INFO": 1
        },
        "events_by_source": {
            "api": 1
        },
        "top_error_sources": {
            "api": 1
        },
        "first_timestamp": "2026-10-13T11:55:00",
        "last_timestamp": "2026-10-13T11:55:00"
    }


def test_valid_cli_jsonl_no_output(capsys, tmp_path):
    file = Path(tmp_path/"data_for_valid_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "INFO", "source": "api", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    main(["analyze", str(file), "--format", "jsonl"])
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "total_events": 1,
        "events_by_level": {
            "INFO": 1
        },
        "events_by_source": {
            "api": 1
        },
        "top_error_sources": {
            "api": 1
        },
        "first_timestamp": "2026-10-13T12:00:00",
        "last_timestamp": "2026-10-13T12:00:00"
    }


def test_valid_cli_csv_output(tmp_path):
    input_file = Path(tmp_path/"data_for_valid_tests.csv")

    input_file.write_text("timestamp,level,source,message\n"
                          "2026-10-13T11:55:00,INFO,api,Запуск API\n",
                          encoding="utf-8")

    main(["analyze", str(input_file), "--format",
         "csv", "--output", "test_cli.csv"])

    assert json.loads(Path("reports/test_cli.csv").read_text(encoding="utf-8")) == {
        "total_events": 1,
        "events_by_level": {
            "INFO": 1
        },
        "events_by_source": {
            "api": 1
        },
        "top_error_sources": {
            "api": 1
        },
        "first_timestamp": "2026-10-13T11:55:00",
        "last_timestamp": "2026-10-13T11:55:00"
    }


def test_valid_cli_jsonl_output(tmp_path):
    file = Path(tmp_path/"data_for_valid_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "INFO", "source": "api", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    main(["analyze", str(file), "--format", "jsonl", "--output", "test_cli.jsonl"])

    assert json.loads(Path("reports/test_cli.jsonl").read_text(encoding="utf-8")) == {
        "total_events": 1,
        "events_by_level": {
            "INFO": 1
        },
        "events_by_source": {
            "api": 1
        },
        "top_error_sources": {
            "api": 1
        },
        "first_timestamp": "2026-10-13T12:00:00",
        "last_timestamp": "2026-10-13T12:00:00"
    }


def test_invalid_cli_csv_no_output(tmp_path):
    file = Path(tmp_path/"data_for_invalid_level_tests.csv")

    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-13T11:55:00,IMFO,api,Запуск API\n",
        encoding="utf -8"
    )

    with pytest.raises(InvalidEventError):
        main(["analyze", str(file), "--format", "csv"])


def test_invalid_cli_jsonl_no_output(tmp_path):
    file = Path(tmp_path/"data_for_invalid_level_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "IMFO", "source": "api", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    with pytest.raises(InvalidEventError):
        main(["analyze", str(file), "--format", "jsonl"])


def test_invalid_cli_csv_output(tmp_path):
    file = Path(tmp_path/"data_for_invalid_level_tests.csv")
    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-13T11:55:00,IMFO,api,Запуск API\n",
        encoding="utf -8"
    )
    with pytest.raises(InvalidEventError):
        main(["analyze", str(file), "--format", "csv",
             "--output", "test_invalid_cli.csv"])


def test_invalid_cli_jsonl_output(tmp_path):
    file = Path(tmp_path/"data_for_invalid_level_tests.jsonl")

    file.write_text(json.dumps({"timestamp": "2026-10-13T12:00:00", "level": "IMFO", "source": "api", "message": "Сервис запущен"},
                               ensure_ascii=False), encoding="utf-8")

    with pytest.raises(InvalidEventError):
        main(["analyze", str(file), "--format", "jsonl",
             "--output", "test_invalid_cli.jsonl"])


def test_cli_csv_skip_invalid(capsys):
    main(["analyze", "tests_invalid_data/skip_invalid_test_large.csv",
         "--format", "csv", "--skip-invalid"])
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "total_events": 103,
        "events_by_level": {
            "INFO": 20,
            "WARNING": 20,
            "ERROR": 19,
            "CRITICAL": 21,
            "DEBUG": 23
        },
        "events_by_source": {
            "worker": 20,
            "database": 20,
            "auth": 19,
            "scheduler": 21,
            "api": 23
        },
        "top_error_sources": {
            "api": 23,
            "scheduler": 21,
            "worker": 20,
            "database": 20,
            "auth": 19
        },
        "first_timestamp": "2026-10-13T09:01:00",
        "last_timestamp": "2026-10-13T11:00:00"
    }


def test_cli_skip_invalid(capsys):
    main(["analyze", "tests_invalid_data/skip_invalid_test_large.jsonl",
         "--format", "jsonl", "--skip-invalid"])
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "total_events": 103,
        "events_by_level": {
            "INFO": 20,
            "WARNING": 20,
            "ERROR": 19,
            "CRITICAL": 21,
            "DEBUG": 23
        },
        "events_by_source": {
            "worker": 20,
            "database": 20,
            "auth": 19,
            "scheduler": 21,
            "api": 23
        },
        "top_error_sources": {
            "api": 23,
            "scheduler": 21,
            "worker": 20,
            "database": 20,
            "auth": 19
        },
        "first_timestamp": "2026-10-13T09:01:00",
        "last_timestamp": "2026-10-13T11:00:00"
    }


def test_cli_config_error():
    with pytest.raises(CLIConfigError):
        main(["analyze", "--format", "csv"])
