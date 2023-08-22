import logging
import os

import bibtexparser
import yaml

_log = logging.getLogger("textbook_assembler")


def load_reference_list(path):
    with open(path) as file:
        refs = yaml.safe_load(file)

    return refs


def get_pdf_names(path):
    all_pdfs = os.listdir(path)
    return all_pdfs


def find_by_full_name(file_name, all_files):
    file_name_lower = file_name.lower()
    all_files_lower = [fname.lower() for fname in all_files]

    if file_name_lower in all_files_lower:
        idx = all_files_lower.index(file_name_lower)
        return all_files[idx]

    return


def find_by_partial_name(file_name, all_files):
    assert file_name.endswith("...")

    file_name_lower = file_name.lower().replace("...", "")
    all_files_lower = [fname.lower() for fname in all_files]

    matches = [
        (idx, file) for idx, file in enumerate(all_files_lower) if file.startswith(file_name_lower)
    ]
    if len(matches) > 1:
        match_names = [name for _, name in matches]
        raise ValueError(
            f'Ambiguous partial file name, found two possible matches: {", ".join(match_names)}'
        )
    elif len(matches) == 0:
        return
    else:
        idx, name_lower = matches[0]
        return all_files[idx]


def load_bibtex_data(bibtex_path):
    with open(bibtex_path) as file:
        bibtex_data = bibtexparser.load(file)

    return bibtex_data


def match_references_to_pdf_filenames(refs, all_files):
    out = {}
    for ref, maybe_path in refs.items():
        f = find_by_partial_name if maybe_path.endswith("...") else find_by_full_name
        full_name = f(maybe_path, all_files)
        if full_name is None:
            raise ValueError(
                f"{maybe_path} not found among PDF files in source directory. Check for typos?"
            )
        out[ref] = full_name

    return out


def get_referenced_bibtex_data(bibtex_data, ref_dict):
    bibtex_dict = bibtex_data.entries
    bibtex_ids = [item.get("ID", None) for item in bibtex_dict]
    ref_set = set(ref_dict.keys())
    id_set = set(bibtex_ids)
    missing = ref_set - id_set
    extras = id_set - ref_set
    referenced = ref_set.intersection(id_set)

    if len(missing) > 0:
        _log.warning(
            "The following references from your reference yaml were not found in the provided bibtex: "
            f'{", ".join(missing)}. It will not be possible to generate references for these resources on'
            " weekly cover sheets"
        )

    if len(extras) > 0:
        _log.warning(
            "The following bibtex references were not found among the provided reference yaml: "
            f'{", ".join(extras)}. They will not be used anywhere in the construction of the final PDF. Do'
            f"you still need them?"
        )
    out = {}
    for ref in bibtex_dict:
        if ref["ID"] in referenced:
            temp = ref.copy()
            del temp["ID"]
            out[ref["ID"]] = temp
    return out
