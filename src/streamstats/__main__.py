import argparse
import sys


from .analysis import Analyzer
from .errors import StreamStatsError, InvalidEventError, UnsupportedFormatError, CLIConfigError
from .parsers import csv_parser, jsonl_parser
from .report import report


def parser(argv=None):
    format = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        prog="streamstats",
        description=(

        ),
        epilog=(
            "\n"
            "\n"
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
            "\n"
            "\n"
        ),
        epilog=(
            "\n"
            "\n"
        ),
        help=(
            "\n"
        ),
        formatter_class=format
    )

    analyzer.add_argument(
        "INPUT",
        # принять одно или более значений
        nargs="+",
        help="files to analyze"
    )

    analyzer.add_argument(
        "--format",
        dest="file_format",
        nargs='+',
        help=""
    )

    analyzer.add_argument(
        "--output",
        dest="output_file",
        help=""
    )
    return parser.parse_args(argv)


def main(argv=None):
    count=-1
    args = parser(argv)
    analyzer = Analyzer()
    if args.command == "analyze":
        for file in args.INPUT:
            count+=1
            if file.endswith(".jsonl") and args.file_format[count]=="jsonl":
                for event in jsonl_parser(file):
                    analyzer.add(event)

            elif file.endswith(".csv") and args.file_format[count]=="csv":
                for event in csv_parser(file):
                    analyzer.add(event)

            else:
                raise UnsupportedFormatError("File format and --format argument doesn't match")
                #уточнить правильный ли вывод ошибки
                

    else:
        #написать ловлю ошибки
        pass
    return report(analyzer.build(), args.output_file)

if __name__ == "__main__":
    main()
