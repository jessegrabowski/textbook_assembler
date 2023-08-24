import logging
import os

import dateutil
import pandas as pd
import pypdf
from unidecode import unidecode_expect_ascii

from textbook_assembler.utils.constants import EXPECTED_DTYPES, EXPECTED_KEYS
from textbook_assembler.utils.references import (
    get_pdf_names,
    get_referenced_bibtex_data,
    load_bibtex_data,
    load_reference_list,
    match_references_to_pdf_filenames,
)

_log = logging.getLogger("textbook_assembler")


def load_input_data(path):
    data = pd.read_csv(path)
    data = lowercase_columns(data)
    data = convert_date_column(data)
    data = drop_empty_rows(data)

    return data


def drop_empty_rows(data):
    return data.dropna(axis=1, how="all")


def convert_date_column(data):
    col = [col for col in data.columns if col == "date"][0]
    data[col] = data[col].map(dateutil.parser.parse)
    return data


def clean_string_data(data):
    cols = [col for col in data.columns if col in ["topic", "reference"]]
    data[cols] = data[cols].applymap(unidecode_expect_ascii)
    return data


def validate_column_names(data):
    data_columns = set(data.columns)
    missing = set(EXPECTED_KEYS) - data_columns
    if len(missing) > 0:
        raise KeyError(f'PDF data is missing the following columns: {", ".join(missing)}')

    extra = data_columns - set(EXPECTED_KEYS)
    if len(extra) > 0:
        _log.warning(f'Dropping unexpected columns from lesson plan CSV: {", ".join(extra)}')
        data.drop(columns=list(extra), inplace=True)


def validate_datatypes(data):
    invalid_cols = {}
    for column in data.columns:
        col_type = EXPECTED_DTYPES[column]

        if data[column].dtype != col_type:  # and (col_type in (float, int)):
            try:
                data[column].astype(col_type)
            except Exception as e:
                invalid_cols[column] = data[column].dtype

    if len(invalid_cols) > 0:
        error_msg = "Found columns with unexpected datatypes that could not be converted: "
        for col, found_dtype in invalid_cols.items():
            expected_dtype = EXPECTED_DTYPES[col]
            error_msg += f"{col}, found: {found_dtype}, expected: {expected_dtype} "

        raise ValueError(error_msg.strip())


def lowercase_columns(data):
    data.columns = [x.lower() for x in data.columns]
    return data


def fill_page_numbers(data, pdf_path):
    cache = {}
    data_out = data.copy()
    data_out.page_start = data_out.page_start.fillna(0)

    missing = data.loc[data.page_end.isna(), "filename"].unique()
    nan_mask = data_out.page_end.isna()
    for pdf_file in missing:
        reader = pypdf.PdfReader(os.path.join(pdf_path, pdf_file))
        cache[pdf_file] = len(reader.pages)
    data_out.loc[nan_mask, "page_end"] = data_out.loc[nan_mask, "filename"].apply(cache.get)

    return data_out


def add_filename_to_data(data, ref_dict, pdf_files):
    out = data.copy()
    matched_refs = match_references_to_pdf_filenames(ref_dict, pdf_files)
    out["filename"] = out["reference"].apply(matched_refs.get)
    return out


def add_bibtext_to_data(data, bibtex_data):
    out = data.copy()
    df_bibtex = pd.DataFrame(bibtex_data).T
    data_refs = set(data.reference)
    bibtex_ids = set(df_bibtex.index)

    missing = data_refs - bibtex_ids
    if len(missing) > 0:
        raise ValueError(
            "The following references found in your lesson plan do not have bibtex entries: "
            f"{', '.join(missing)}"
        )

    out = out.merge(df_bibtex, left_on="reference", right_index=True, how="left")

    return out


def load_and_process_data(path, pdf_path=None, reference_path=None, bibtex_path=None):
    ref_dict = {}

    data = load_input_data(path)
    validate_column_names(data)
    validate_datatypes(data)
    data = clean_string_data(data)

    if reference_path:
        pdf_files = get_pdf_names(pdf_path)
        ref_dict = load_reference_list(reference_path)
        data = add_filename_to_data(data, ref_dict, pdf_files)
        data = fill_page_numbers(data, pdf_path)

    if bibtex_path:
        bibtext_dict = load_bibtex_data(bibtex_path)
        if reference_path:
            bibtext_dict = get_referenced_bibtex_data(bibtext_dict, ref_dict)
        data = add_bibtext_to_data(data, bibtext_dict)

    return data
