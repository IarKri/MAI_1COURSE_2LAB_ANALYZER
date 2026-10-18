from pathlib import Path


from streamstats.parsers import csv_parser, jsonl_parser


def test_empty_jsonl_file():

    file=Path("tests_valid_data/empty_file_for_test.jsonl")
    for event in jsonl_parser(file, None, 0):
        assert event == []

def test_empty_csv_file():

    file=Path("tests_valid_data/empty_file_for_test.csv")
    for event in csv_parser(file, None, 0):
        assert event == []