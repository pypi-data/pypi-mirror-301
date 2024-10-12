import argparse
import sys

from marko import Markdown

from .obsidian2html import obsidian2html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Translate and Obsidian markdown file to HTML"
    )

    parser.add_argument(
        "src",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Markdown source file to convert to HTML (default stdin)",
    )
    parser.add_argument(
        "dst",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Destination file to write HTML output to (default stdout)",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    args.outfile.write(obsidian2html(args.infile.read()))

    return 0
