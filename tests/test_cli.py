import json
import pytest
from pathlib import Path


from streamstats.__main__ import main
from streamstats.errors import InvalidEventError, CLIConfigError


def test_valid_cli_csv_no_output(capsys):

    main(["analyze", "tests_valid_data/data_for_valid_tests.csv", "--format", "csv"])
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

def test_valid_cli_jsonl_no_output(capsys):

    main(["analyze", "tests_valid_data/data_for_valid_tests.jsonl", "--format", "jsonl"])
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

def test_valid_cli_csv_output():


    main(["analyze", "tests_valid_data/data_for_valid_tests.csv", "--format", "csv", "--output", "test_cli.csv"])

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

def test_valid_cli_jsonl_output():


    main(["analyze", "tests_valid_data/data_for_valid_tests.jsonl", "--format", "jsonl", "--output", "test_cli.jsonl"])

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

def test_invalid_cli_csv_no_output():
    with pytest.raises(InvalidEventError):
        main(["analyze", "tests_invalid_data/data_for_invalid_level_tests.csv", "--format", "csv"])

def test_invalid_cli_jsonl_no_output():
    with pytest.raises(InvalidEventError):
        main(["analyze", "tests_invalid_data/data_for_invalid_level_tests.jsonl", "--format", "jsonl"])  

def test_invalid_cli_csv_output():
    with pytest.raises(InvalidEventError):
        main(["analyze", "tests_invalid_data/data_for_invalid_level_tests.csv", "--format", "csv", "--output", "test_invalid_cli.csv"])

def test_invalid_cli_jsonl_output():
    with pytest.raises(InvalidEventError):
        main(["analyze", "tests_invalid_data/data_for_invalid_level_tests.jsonl", "--format", "jsonl", "--output", "test_invalid_cli.jsonl"])

def test_cli_csv_skip_invalid(capsys):
    main(["analyze", "tests_invalid_data/skip_invalid_test_large.csv", "--format", "csv", "--skip-invalid"])
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
    main(["analyze", "tests_invalid_data/skip_invalid_test_large.jsonl", "--format", "jsonl", "--skip-invalid"])
    captured=capsys.readouterr()
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
