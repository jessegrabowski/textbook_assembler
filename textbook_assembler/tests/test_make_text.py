from textbook_assembler.utils.make_text import assemble_textbook


def test_get_pdf_slice():
    bibtex_path = "textbook_assembler/tests/resources/bibtex/test2.bib"
    ref_path = "textbook_assembler/tests/resources/config/ref_to_file.yaml"
    data_path = "textbook_assembler/tests/resources/csvs/test_complete.csv"
    pdf_path = "textbook_assembler/tests/resources/pdfs"

    assemble_textbook(data_path, pdf_path, ref_path, bibtex_path, out_path="output/textbook.pdf")
