import pytest

from textbook_assembler.utils.references import (
    find_by_full_name,
    find_by_partial_name,
    get_pdf_names,
    get_referenced_bibtex_data,
    load_bibtex_data,
    load_reference_list,
    match_references_to_pdf_filenames,
)


def test_load_reference_yaml():
    ref_dict = load_reference_list("textbook_assembler/tests/resources/config/ref_to_file.yaml")
    assert type(ref_dict) == dict
    assert len(ref_dict) == 5


def test_load_filenames():
    files = get_pdf_names("textbook_assembler/tests/resources/pdfs")
    expected = [
        "GLS_Intermediate_Macro.pdf",
        "rbc_extensions_sp17.pdf",
        "rbc_notes_2017.pdf",
        "stylized_facts_rbc_sp17.pdf",
        "uribe-notes.pdf",
    ]

    assert all([file in expected for file in files])


@pytest.mark.parametrize(
    "fname, expected",
    [("rbc_notes_2017.pdf", "rbc_notes_2017.pdf"), ("rbc_notes_2017", None)],
    ids=["match", "no_match"],
)
def test_find_by_full_name(fname, expected):
    all_files = get_pdf_names("textbook_assembler/tests/resources/pdfs")
    res = find_by_full_name(fname, all_files)
    assert res == expected


@pytest.mark.parametrize(
    "fname, expected", [("rbc...", None), ("rbc_notes...", "rbc_notes_2017.pdf")]
)
def test_find_by_partial_name(fname, expected):
    all_files = get_pdf_names("textbook_assembler/tests/resources/pdfs")
    if expected is None:
        with pytest.raises(ValueError, match="Ambiguous partial file name"):
            find_by_partial_name(fname, all_files)
    else:
        res = find_by_partial_name(fname, all_files)
        assert res == expected


def test_match_references_to_pdf_filenames():
    ref_dict = load_reference_list("textbook_assembler/tests/resources/config/ref_to_file.yaml")
    all_pdf_files = get_pdf_names("textbook_assembler/tests/resources/pdfs")

    matched_refs = match_references_to_pdf_filenames(ref_dict, all_pdf_files)
    expected = {
        "GLS": "GLS_Intermediate_Macro.pdf",
        "U": "uribe-notes.pdf",
        "S1": "rbc_notes_2017.pdf",
        "S2": "stylized_facts_rbc_sp17.pdf",
        "SE": "rbc_extensions_sp17.pdf",
    }

    assert all([value == expected[key] for key, value in matched_refs.items()])


def test_load_bibtex():
    bibtext_dict = load_bibtex_data("textbook_assembler/tests/resources/bibtex/test1.bib")
    assert len(bibtext_dict.entries) == 6


@pytest.mark.parametrize(
    "error",
    [
        "The following references from your reference yaml were not found",
        "The following bibtex references were not found among the provided reference yaml",
    ],
    ids=["missing", "extra"],
)
def test_extra_bibtex_references_warns(error, caplog):
    bibtext_dict = load_bibtex_data("textbook_assembler/tests/resources/bibtex/test1.bib")
    ref_dict = load_reference_list("textbook_assembler/tests/resources/config/ref_to_file.yaml")

    _ = get_referenced_bibtex_data(bibtext_dict, ref_dict)
    assert any([record.getMessage().startswith(error) for record in caplog.records])


def test_get_referenced_bibtex():
    bibtext_dict = load_bibtex_data("textbook_assembler/tests/resources/bibtex/test2.bib")
    ref_dict = load_reference_list("textbook_assembler/tests/resources/config/ref_to_file.yaml")

    referenced_bibtex = get_referenced_bibtex_data(bibtext_dict, ref_dict)

    assert len(referenced_bibtex) == len(ref_dict)
    assert (set(referenced_bibtex.keys()) - set(ref_dict.keys())) == set()
