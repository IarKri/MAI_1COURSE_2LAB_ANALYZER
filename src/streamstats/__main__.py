import argparse
import sys


from .analysis import Analyzer
from .errors import (
    StreamStatsError,
    UnsupportedFormatError,
    UnmatchedFormatsError,
)
from .parsers import csv_parser, jsonl_parser
from .report import report


def parser(argv=None):
    '''
    Формирует парсер аргументов
    
    Args:
        Argv: Аргументы, подающиеся на вход
        
    Returns:
        argparse.Namespace: объект с указанными полями 
    '''
    format = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        prog="streamstats",
        description=(
            "Files analyzer\n"
            "Supports analyzing files with format .csv and .jsonl"
        ),
        epilog=(
            "Examples:\n"
            "python -m streamstats analyze path.csv --format csv\n"
            "python -m streamstats analyze path.json path.csv --format json csv\n"
            "python -m streamstats analyze path.json --skip-invalid"
        ),
        formatter_class=format
    )

    subparser = parser.add_subparsers(
        dest="command",
        required=True,
        title="Set of commands"
    )

    analyzer = subparser.add_parser(
        "analyze",
        description=(
            "Analyzer\n"
            "Supports analyzing of multiple csv and json files\n"
        ),
        help="analyzing",
        formatter_class=format
    )

    analyzer.add_argument(
        "INPUT",
        # принять одно или более значений
        nargs="+",
        help="files to analyze (supporting multiple files)"
    )

    analyzer.add_argument(
        "--format",
        dest="file_format",
        nargs='+',
        help="file format (supproting only .csv and .json files)"
    )

    analyzer.add_argument(
        "--output",
        dest="output_file",
        help="file to import result"
    )
    return parser.parse_args(argv)


def main(argv=None):
    """
    Запускает работу всей программы

    Args:
        argv: Аргументы, подающиеся на вход
    """
    count=-1
    args = parser(argv)
    analyzer = Analyzer()
    if args.command == "analyze":
        for file in args.INPUT:
            if not file.endswith(".jsonl") and not file.endswith(".csv"):
                raise UnsupportedFormatError("Unsupported File Format")
            count+=1
            if file.endswith(".jsonl") and args.file_format[count]=="jsonl":
                for event in jsonl_parser(file):
                    analyzer.add(event)

            elif file.endswith(".csv") and args.file_format[count]=="csv":
                for event in csv_parser(file):
                    analyzer.add(event)

            else:
                raise UnmatchedFormatsError("File format and --format argument doesn't match")
                #уточнить правильный ли вывод ошибки
                

    else:
        #написать ловлю ошибки
        pass
    return report(analyzer.build(), args.output_file)

if __name__ == "__main__":
    try:
        main()
    except StreamStatsError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(2)
