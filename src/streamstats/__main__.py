import argparse
import sys

from src.streamstats.analysis import analyzer

def parser(argv=None):
    format = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        prog="streamstats",
        description=(
    
        ),
        epilog=(

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

        ),
        epilog=(

        ),
        help=(

        ),
    formatter_class=format
    )

    analyzer.add_argument(
        "INPUT",
        #принять одно или более значений
        nargs="+",
        help="files to analyze"
    )

    return parser.parse_args(argv)


def main():
    args = parser
    result = analyzer(parse_files(files))
    print(result)


if __name__ == "__main__":
    main()