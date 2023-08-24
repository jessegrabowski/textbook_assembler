import datetime

import pandas as pd
import pytest

from textbook_assembler.utils.constants import EXPECTED_DTYPES, EXPECTED_KEYS
from textbook_assembler.utils.data import (
    add_bibtext_to_data,
    add_filename_to_data,
    convert_date_column,
    fill_page_numbers,
    load_and_process_data,
)
from textbook_assembler.utils.references import (
    get_pdf_names,
    get_referenced_bibtex_data,
    load_bibtex_data,
    load_reference_list,
)


def test_load_data_fails_if_columns_missing():
    with pytest.raises(KeyError, match="PDF data is missing the following columns: page_end"):
        data = load_and_process_data("textbook_assembler/tests/resources/csvs/test1.csv")


def test_extra_columns_dropped():
    data = load_and_process_data("textbook_assembler/tests/resources/csvs/test2.csv")
    assert "extra_column" not in data.columns


def test_load_data_fails_with_bad_dtypes():
    with pytest.raises(
        ValueError,
        match=f"Found columns with unexpected datatypes that could not be converted: "
        f"page_end, found: object, expected: float64",
    ):
        data = load_and_process_data(f"textbook_assembler/tests/resources/csvs/test3.csv")


@pytest.mark.parametrize(
    "data",
    [
        pd.DataFrame([{"date": "Sept-13-2023"}]),
        pd.DataFrame([{"date": "Sept-13"}]),
        pd.DataFrame([{"date": "09-13"}]),
    ],
    ids=["well_formed", "no_year", "no_year_int"],
)
def test_datetime_convert(data):
    data = convert_date_column(data)
    assert data["date"].dt.month.values[0] == 9
    assert data["date"].dt.day.values[0] == 13
    assert data["date"].dt.year.values[0] == datetime.datetime.now().year


def test_fill_page_numbers():
    pdf_path = "textbook_assembler/tests/resources/pdfs"
    data = pd.DataFrame([{"filename": "rbc_notes_2017.pdf", "page_start": None, "page_end": None}])

    data = fill_page_numbers(data, pdf_path)

    assert data.loc[0, "page_start"] == 0
    assert data.loc[0, "page_end"] == 25


def test_convert_dtype_preserves_missing():
    data = pd.DataFrame([{"chapter": None}])


def test_add_filename_to_data():
    data = load_and_process_data("textbook_assembler/tests/resources/csvs/input_data.csv")
    ref_dict = load_reference_list("textbook_assembler/tests/resources/config/ref_to_file.yaml")
    pdf_files = get_pdf_names("textbook_assembler/tests/resources/pdfs")

    new_data = add_filename_to_data(data, ref_dict, pdf_files)
    assert "filename" in new_data.columns
    assert (set(new_data.columns) - set(data.columns)) == {"filename"}
    assert new_data.shape[0] == data.shape[0]


def test_add_bibtex_to_data():
    data = load_and_process_data("textbook_assembler/tests/resources/csvs/test_complete.csv")
    bibtext_dict = load_bibtex_data("textbook_assembler/tests/resources/bibtex/test2.bib")
    ref_dict = load_reference_list("textbook_assembler/tests/resources/config/ref_to_file.yaml")

    referenced_bibtex = get_referenced_bibtex_data(bibtext_dict, ref_dict)
    new_data = add_bibtext_to_data(data, referenced_bibtex)

    assert all(
        [
            key in new_data.columns
            for key in ["ENTRYTYPE", "title", "author", "howpublished", "journal"]
        ]
    )
    for ref in referenced_bibtex.keys():
        test_row = new_data.loc[new_data.reference == ref].iloc[0].to_dict()
        keys = referenced_bibtex[ref].keys()
        assert all([test_row[k] == referenced_bibtex[ref][k] for k in keys])


@pytest.mark.parametrize(
    "data_path",
    [
        "textbook_assembler/tests/resources/csvs/test_complete.csv",
        "textbook_assembler/tests/resources/csvs/test_complete_w_indexcol.csv",
    ],
    ids=["no_index", "index"],
)
def test_load_data(data_path):
    pdf_path = "textbook_assembler/tests/resources/pdfs"
    reference_path = "textbook_assembler/tests/resources/config/ref_to_file.yaml"
    bibtex_path = "textbook_assembler/tests/resources/bibtex/test2.bib"
    data = load_and_process_data(data_path, pdf_path, reference_path, bibtex_path)

    dtype_dict = data[EXPECTED_KEYS].dtypes

    assert hasattr(data.date.dt, "day_name")
    assert all([x in data.columns.str.lower() for x in EXPECTED_KEYS])
    assert all([dtype == EXPECTED_DTYPES[col.lower()] for col, dtype in dtype_dict.items()])
    assert (
        not data[["week", "date", "topic", "reference", "page_start", "page_end"]]
        .isna()
        .any()
        .any()
    )
