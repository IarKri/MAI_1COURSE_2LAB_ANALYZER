from pathlib import Path


from streamstats.analysis import Analyzer
from streamstats.models import Level
from streamstats.parsers import csv_parser, jsonl_parser
from streamstats.report import report


def test_empty_jsonl_file():

    file=Path("tests_data/empty_file_for_test.jsonl")
    for event in jsonl_parser(file):
        assert event == []

def test_empty_csv_file():

    file=Path("tests_data/empty_file_for_test.csv")
    for event in csv_parser(file):
        assert event == []