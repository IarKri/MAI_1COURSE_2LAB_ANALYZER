from streamstats.analysis import Analyzer
from streamstats.parsers import jsonl_parser
from streamstats.parsers import csv_parser


def test_valid_jsonl_parser():
    events=jsonl_parser("tests_data/test_events.jsonl")

    analyzer=Analyzer()
    for event in events:
        analyzer.add(event)

    actual = analyzer.build()

    expected = {
    "total_events": 15,
    "events_by_level": {
        "INFO": 4,
        "ERROR": 5,
        "WARNING": 2,
        "CRITICAL": 3,
        "DEBUG": 1
    },
    "events_by_source": {
        "api": 4,
        "database": 4,
        "worker": 3,
        "auth": 2,
        "server": 2
    },
    "top_error_sources": {
        "api": 4,
        "database": 4,
        "worker": 3,
        "auth": 2,
        "server": 2
    },
    "first_timestamp": "2026-10-13T11:55:00",
    "last_timestamp": "2026-10-13T13:00:00"
    }

    assert actual==expected

def test_csv_parser_comma():
    events=csv_parser("tests_data/test_events_comma.csv")
    analyzer=Analyzer()
    for event in events:
        analyzer.add(event)
    
    actual = analyzer.build()

    expected = {
    "total_events": 15,
    "events_by_level": {
        "INFO": 4,
        "DEBUG": 1,
        "WARNING": 2,
        "ERROR": 5,
        "CRITICAL": 3
    },
    "events_by_source": {
        "api": 4,
        "worker": 3,
        "database": 5,
        "auth": 1,
        "server": 2
    },
    "top_error_sources": {
        "database": 5,
        "api": 4,
        "worker": 3,
        "server": 2,
        "auth": 1
    },
    "first_timestamp": "2026-10-13T11:55:00",
    "last_timestamp": "2026-10-13T13:00:00"
    }

    assert actual == expected

def test_csv_parser_semicolon():
    events=csv_parser("test_data/test_events_semicolon.csv")
    analyzer=Analyzer()
    for event in events:
        analyzer.add(event)

    actual = analyzer.build()

    expected={
    "total_events": 7,
    "events_by_level": {
        "INFO": 2,
        "ERROR": 2,
        "WARNING": 1,
        "CRITICAL": 1,
        "DEBUG": 1
    },
    "events_by_source": {
        "api": 2,
        "cache": 1,
        "database": 2,
        "worker": 2
    },
    "top_error_sources": {
        "api": 2,
        "database": 2,
        "worker": 2,
        "cache": 1
    },
    "first_timestamp": "2026-10-14T09:00:00",
    "last_timestamp": "2026-10-14T09:06:00"
    }

    assert actual==expected