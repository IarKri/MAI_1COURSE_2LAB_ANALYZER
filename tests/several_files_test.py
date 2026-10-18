from pathlib import Path

from streamstats.analysis import Analyzer
from streamstats.parsers import jsonl_parser
from streamstats.parsers import csv_parser


def test_several_files_analyzing():

    analyzer=Analyzer()

    file_jsonl = Path("tests_valid_data/data_for_valid_tests.jsonl")
    for event in jsonl_parser(file_jsonl, None, 0):
        analyzer.add(event)

    file_csv=Path("tests_valid_data/data_for_valid_tests.csv")

    for event in csv_parser(file_csv, None, 0):
        analyzer.add(event)

    assert analyzer.build() == {
    "total_events": 2,
    "events_by_level": {
        "INFO": 2
    },
    "events_by_source": {
        "api": 2
    },
    "top_error_sources": {
        "api": 2
    },
    "first_timestamp": "2026-10-13T11:55:00",
    "last_timestamp": "2026-10-13T12:00:00"
    }