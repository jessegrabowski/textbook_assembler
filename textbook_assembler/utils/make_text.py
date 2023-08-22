import os
import tempfile

from pypdf import PdfWriter

from textbook_assembler.utils.data import load_and_process_data
from textbook_assembler.utils.latex import generate_weekly_cover_sheets


def read_pages_from_pdf(writer, row, pdf_path):
    start_page = max(0, int(row["page_start"]) - 1)
    end_page = int(row["page_end"])
    pdf_fname = row["filename"]

    if pdf_fname is None:
        return

    fname = os.path.join(pdf_path, pdf_fname)

    with open(fname, "rb") as file:
        page_slice = (start_page, end_page)
        writer.append(file, pages=page_slice)


def make_output_dir(dir="output"):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def assemble_textbook(data_path, pdf_path, ref_path, bibtex_path, out_path):
    data = load_and_process_data(data_path, pdf_path, ref_path, bibtex_path)
    merger = PdfWriter()
    out_dir, out_fname = os.path.split(out_path)

    with tempfile.TemporaryDirectory() as tempdir:
        cover_sheets = generate_weekly_cover_sheets(data, bibtex_path, out_path=tempdir)
        weekly_data = data.groupby("week")

        for cover_sheet, (week, group) in zip(cover_sheets, weekly_data):
            merger.append(cover_sheet)
            for idx, row in group.iterrows():
                read_pages_from_pdf(merger, row, pdf_path)

        make_output_dir(out_dir)

        with open(out_path, "wb") as file:
            merger.write(file)
