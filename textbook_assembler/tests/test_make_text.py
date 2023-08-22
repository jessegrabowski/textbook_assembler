import os

import pypdf

from textbook_assembler.utils.data import load_and_process_data
from textbook_assembler.utils.make_text import assemble_textbook


def _get_expected_pages(data_path, pdf_path, ref_path, bibtex_path):
    data = load_and_process_data(data_path, pdf_path, ref_path, bibtex_path)
    n_pages = (data["page_end"] - data["page_start"] + 1).sum()
    n_pages += data.week.unique().shape[0] - 1

    return n_pages


def test_assemble_textbook(tmpdir):
    bibtex_path = "textbook_assembler/tests/resources/bibtex/test2.bib"
    ref_path = "textbook_assembler/tests/resources/config/ref_to_file.yaml"
    data_path = "textbook_assembler/tests/resources/csvs/test_complete.csv"
    pdf_path = "textbook_assembler/tests/resources/pdfs"
    out_path = f"{tmpdir}/textbook.pdf"

    assemble_textbook(data_path, pdf_path, ref_path, bibtex_path, out_path=out_path)
    assert os.path.isfile(out_path)

    n_pages_out = len(pypdf.PdfReader(out_path).pages)
    n_expected_pages = _get_expected_pages(data_path, pdf_path, ref_path, bibtex_path)

    assert n_pages_out == n_expected_pages
