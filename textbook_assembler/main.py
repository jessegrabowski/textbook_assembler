import argparse
import logging
import sys
from typing import Sequence

from textbook_assembler.utils.make_text import assemble_textbook

_log = logging.getLogger("textbook_assembler")


def parse_args(args: Sequence[str] = None):
    if args is None:
        args = []

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lesson_path",
        "-l",
        type=str,
        required=False,
        default="materials/lesson_plan.csv",
        help="Path to the CSV file containing the lesson plan for the textbook",
    )
    parser.add_argument(
        "--source_dir",
        "-s",
        type=str,
        required=False,
        default="materials/pdfs",
        help="Path to directory containing PDFs to be assembled",
    )
    parser.add_argument(
        "--output_path",
        "-o",
        type=str,
        required=False,
        default="materials/output/textbook.pdf",
        help="Output path for the assembled textbook",
    )
    parser.add_argument(
        "--bibtex_path",
        "-b",
        type=str,
        required=False,
        default="materials/citations.bib",
        help="Path a bibtex file containing reference information for the PDFs in the lesson plan",
    )
    parser.add_argument(
        "--ref_path",
        "-r",
        type=str,
        required=False,
        default="materials/ref_to_file.yaml",
        help="Path to YAML with mapping between bibtex references and source files",
    )

    return parser.parse_args(args)


def parsed_args_to_kwargs(parser_args):
    return {
        "data_path": parser_args.lesson_path,
        "pdf_path": parser_args.source_dir,
        "ref_path": parser_args.ref_path,
        "bibtex_path": parser_args.bibtex_path,
        "out_path": parser_args.output_path,
    }


def main():
    args = parse_args(sys.argv[1:])
    kwargs = parsed_args_to_kwargs(args)
    assemble_textbook(**kwargs)
