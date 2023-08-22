import os

from textbook_assembler.utils.data import load_and_process_data
from textbook_assembler.utils.latex import (
    generate_weekly_cover_sheet,
    generate_weekly_cover_sheets,
)


def test_generate_cover_sheet(tmpdir):
    bibtex_path = "textbook_assembler/tests/resources/bibtex/test2.bib"
    ref_path = "textbook_assembler/tests/resources/config/ref_to_file.yaml"
    data_path = "textbook_assembler/tests/resources/csvs/test_complete.csv"
    pdf_path = "textbook_assembler/tests/resources/pdfs"

    data = load_and_process_data(data_path, pdf_path, ref_path, bibtex_path)
    week_data = data[data.week == 4]

    date = week_data.iloc[0]["date"]
    generate_weekly_cover_sheet(4, date, week_data, bibtex_path, out_path=tmpdir)

    assert os.path.isfile(os.path.join(tmpdir, "week_4_coversheet.pdf"))


def test_generate_weekly_cover_sheets(tmpdir):
    bibtex_path = "textbook_assembler/tests/resources/bibtex/test2.bib"
    ref_path = "textbook_assembler/tests/resources/config/ref_to_file.yaml"
    data_path = "textbook_assembler/tests/resources/csvs/test_complete.csv"
    pdf_path = "textbook_assembler/tests/resources/pdfs"

    data = load_and_process_data(data_path, pdf_path, ref_path, bibtex_path)
    generate_weekly_cover_sheets(data, bibtex_path, out_path=tmpdir)

    for week in data.week.unique():
        assert os.path.isfile(os.path.join(tmpdir, f"week_{week}_coversheet.pdf"))
