import os
import shutil

import pandas as pd
from pylatex import (
    Command,
    Document,
    Enumerate,
    NoEscape,
    Package,
    Section,
    escape_latex,
)

from textbook_assembler.utils.constants import EXPECTED_KEYS


def _safe_int(x):
    if x is None or pd.isna(x):
        return None
    elif isinstance(x, str):
        return x
    return max(1, int(x))


def _data_to_bibtex(row):
    bibtex_keys = list(set(row.keys()) - set(EXPECTED_KEYS))
    bibtex_dict = {k: str(row[k]) for k in bibtex_keys}
    bibtex_dict["ID"] = row["reference"]

    return bibtex_dict


def prettify_date(date):
    return f"{date.day_name()}, {date.month_name()} {date.day}, {date.year}"


def data_to_list(data):
    return [d for d in data.T.to_dict().values()]


def hyperlink(url, text):
    text = escape_latex(text)
    return NoEscape(r"\href{" + url + "}{" + text + "}")


def generate_weekly_cover_sheet(week_number, date, data, bibtex_path, out_path=None):
    if out_path is None:
        out_path = ""

    bibtex_file = os.path.split(bibtex_path)[-1]
    shutil.copy(bibtex_path, os.path.join(out_path, bibtex_file))

    doc = Document()
    doc.preamble.append(Package("bibentry"))
    doc.preamble.append(Package("natbib"))
    doc.packages.append(Package("hyperref"))

    topic = getattr(data, "topic", None)
    title = f"Readings for Week {week_number}"

    if topic is not None:
        topic = topic.unique()
        title = f"{title}: {topic[0]}"

    doc.preamble.append(Command("title", title))
    doc.preamble.append(Command("date", prettify_date(date)))
    doc.append(NoEscape(r"\maketitle"))

    with doc.create(Section("Reading Materials")):
        with doc.create(Enumerate()) as enum:
            for row in data_to_list(data):
                row["title"] = row["title"].title()
                elements = map(row.get, ["title", "chapter", "page_start", "page_end"])
                line = ""
                for s, element, suffix in zip(
                    ["", "Chapter", "Pages", "-"], elements, [", ", ", ", " ", ". "]
                ):
                    if element is not None and not pd.isna(element):
                        line += f"{s} {_safe_int(element)}{suffix}"
                if row["url"] is not None and not pd.isna(row["url"]):
                    line += hyperlink(row["url"], "Available here")
                enum.add_item(NoEscape(line))

    for row in data_to_list(data):
        doc.append(Command("bibentry", arguments=[row["reference"]]))

    doc.append(Command("bibliographystyle", arguments=["aer"]))
    doc.append(Command("bibliography", arguments=[NoEscape(bibtex_file.replace(".bib", ""))]))

    filepath = os.path.join(out_path, f"week_{week_number}_coversheet")
    doc.generate_pdf(filepath=filepath, clean=True, clean_tex=True)

    return filepath + ".pdf"


def generate_weekly_cover_sheets(data, bibtex_path, out_path=None):
    weekly_data = data.groupby("week")
    paths = []

    for week_number, group in weekly_data:
        date = group.date.unique()[0]
        fpath = generate_weekly_cover_sheet(week_number, date, group, bibtex_path, out_path)
        paths.append(fpath)

    return paths
