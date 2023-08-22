import os
import sys
from unittest.mock import patch

from textbook_assembler.main import main, parse_args


def test_parse_args_with_defaults():
    args = parse_args()
    assert args.lesson_path == "materials/lesson_plan.csv"
    assert args.source_dir == "materials/pdfs"
    assert args.output_path == "materials/output/textbook.pdf"
    assert args.bibtex_path == "materials/bibtex.bib"
    assert args.ref_path == "materials/ref_to_file.yaml"


def test_parse_args():
    bibtex_path = "textbook_assembler/tests/resources/bibtex/test2.bib"
    ref_path = "textbook_assembler/tests/resources/config/ref_to_file.yaml"
    data_path = "textbook_assembler/tests/resources/csvs/test_complete.csv"
    pdf_path = "textbook_assembler/tests/resources/pdfs"
    output_path = "output/textbook.pdf"

    args = ["-l", data_path, "-s", pdf_path, "-o", output_path, "-b", bibtex_path, "-r", ref_path]
    args = parse_args(args)
    keys = ["lesson_path", "source_dir", "output_path", "bibtex_path", "ref_path"]
    for key, value in zip(keys, [data_path, pdf_path, output_path, bibtex_path, ref_path]):
        assert getattr(args, key) == value


def test_main(tmpdir):
    bibtex_path = "textbook_assembler/tests/resources/bibtex/test2.bib"
    ref_path = "textbook_assembler/tests/resources/config/ref_to_file.yaml"
    data_path = "textbook_assembler/tests/resources/csvs/test_complete.csv"
    pdf_path = "textbook_assembler/tests/resources/pdfs"
    output_path = f"{tmpdir}/textbook.pdf"

    test_args = [
        "script_name",
        "-l",
        data_path,
        "-s",
        pdf_path,
        "-o",
        output_path,
        "-b",
        bibtex_path,
        "-r",
        ref_path,
    ]

    with patch.object(sys, "argv", test_args):
        main()

    assert os.path.isfile(output_path)
