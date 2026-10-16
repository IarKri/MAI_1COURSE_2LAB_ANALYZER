from pathlib import Path
import json


from streamstats.__main__ import main


def test_cli_csv_no_output(capsys):

    main(["analyze", "tests_data/data_for_tests.csv", "--format", "csv"])
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

def test_cli_jsonl_no_output(capsys):

    main(["analyze", "tests_data/data_for_tests.jsonl", "--format", "jsonl"])
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

def test_cli_csv_output():
        
    main(["analyze", "tests_data/data_for_tests.csv", "--format", "csv", "--output", "test_cli.csv"])

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

def test_cli_jsonl_output():
    main(["analyze", "tests_data/data_for_tests.jsonl", "--format", "jsonl", "--output", "test_cli.jsonl"])

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

# def test_cli_csv_