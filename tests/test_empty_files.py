from pathlib import Path


from streamstats.parsers import csv_parser, jsonl_parser


def test_empty_jsonl_file(tmp_path):

    file=Path(tmp_path/"test_empty_file.jsonl")

    file.touch()
    for event in list(jsonl_parser(file, None, 0)):
        assert event == []

def test_empty_csv_file(tmp_path):

    file=Path(tmp_path/"test_empty_file.csv")

    file.touch()
    for event in list(csv_parser(file, None, 0)):
        assert event == []