import argparse
import sys


from .analysis import Analyzer
from .errors import (
    CLIConfigError,
    StreamStatsError,
    UnsupportedFormatError,
    UnmatchedFormatsError,
    )
from .models import CustomArgumentParser
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
    parser = CustomArgumentParser(
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
        title="Set of commands",
        parser_class=CustomArgumentParser
    )

    analyzer = subparser.add_parser(
        "analyze",
        description=(
            "Analyzer\n"
            "Supports analyzing of multiple csv and json files\n"
        ),
        help="analyzing csv and jsonl files",
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
        required=True,
        nargs='+',
        help="file format (supproting only .csv and .json files)"
    )

    analyzer.add_argument(
        "--output",
        dest="output_file",
        help = (
        "puts report in your custom file\n",
        "not required function\n",
        "without --output result will be printed in terminal\n",
        )
    )

    analyzer.add_argument(
        "--skip-invalid",
        dest="skip_invalid",
        action="store_true",
        help="passing line with error and writing WARNING in log with information about error"
    )
    return parser.parse_args(argv)


def main(argv=None):
    """
    Запускает работу всей программы

    Args:
        argv: Аргументы, подающиеся на вход
    """
    counter=-1
    try:
        args = parser(argv)
    except CLIConfigError as error:
        raise CLIConfigError(f"{error}")
    analyzer = Analyzer()
    if args.command == "analyze":
        counter+=1
        for file in args.INPUT:
            if not file.endswith(".jsonl") and not file.endswith(".csv"):
                raise UnsupportedFormatError("Unsupported File Format")
            
            if file.endswith(".jsonl") and args.file_format[counter]=="jsonl":
                for event in jsonl_parser(file, counter+1, args.skip_invalid):
                    analyzer.add(event)

            elif file.endswith(".csv") and args.file_format[counter]=="csv":
                for event in csv_parser(file, counter+1, args.skip_invalid):
                    analyzer.add(event)

            elif len(args.INPUT) < len(args.file_format):
                raise UnmatchedFormatsError("Number of --format arguments are bigger than number of files")
            
            else:
                raise UnmatchedFormatsError("File format and --format argument doesn't match")

    return report(analyzer.build(), args.output_file)

if __name__ == "__main__":
    try:
        main()
    except StreamStatsError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(2)
    except Exception as error:
        print(f"Unknown error: {error}", file = sys.stderr)
        sys.exit(2)
