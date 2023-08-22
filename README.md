# Textbook Assembler
A tool for assembling a collection of PDF resources into a single "textbook"

While it's nice to teach from a textbook, the modern teacher has a huge array of resources to pull from, including unpublished notes, lecture slides, and even code repositories. Providing students with these resources as a huge library of PDFs is intimidating, disorienting, and confusing. This is especially true when you don't need the entire resource, only a few pages or slides.

This package aims to solve this problem by giving teachers an easy way to merge a large volume of files into a single "textbook", which can then be distributed to students. References and links are added to ensure proper credit assignment for everything used in the class.

## Usage

Install the package using pip:

```text
pip install textbook-assembler
```

To run the script with default arguments, use:

```text
python -m textbook_assembler
```

The following arguments are available:

```text
python -m textbook_assembler --help

options:
  -h, --help            show this help message and exit
  --lesson_path LESSON_PATH, -l LESSON_PATH
                        Path to the CSV file containing the lesson plan for the textbook
  --source_dir SOURCE_DIR, -s SOURCE_DIR
                        Path to directory containing PDFs to be assembled
  --output_path OUTPUT_PATH, -o OUTPUT_PATH
                        Output path for the assembled textbook
  --bibtex_path BIBTEX_PATH, -b BIBTEX_PATH
                        Path a bibtex file containing reference information for the PDFs in the lesson plan
  --ref_path REF_PATH, -r REF_PATH
                        Path to YAML with mapping between bibtex references and source files
```

The defaults are:

```text
    --lesson_plan materials/lesson_plan.csv
    --source_dir materials/pdfs
    --output_path materials/output/textbook.pdf
    --bibtex_path materials/citations.bib
    --ref_path materials/ref_to_file.yaml
```

## Details and Example

The script requires 4 inputs:

1. A directory of PDF files to be assembled
2. A "lesson plan", a csv file with the following columns: `week, date, topic, reference, chapter, page_start, page_end`
3. A YAML file mapping bibtex reference ids to PDF file names
4. A bibtex file with citations for all documents included in the lesson plan

An example setup is provided in the `materials/` directory.

### Lesson Plan
The lesson plan is the most particular thing required. It should be a CSV file where the rows are class resources, and the columns
are specific metadata about that resource. The required columns are:

1. `week`, the week of the class the resource will be used
2. `date`, the date of the class the resource will be used
3. `topic`, a short description of the topic of the resource
4. `reference`, the bibtex ID for this resource
5. `chapter`, the chapter number of the resource being used
6. `page_start`, the first **pdf page numbered** page students should read
7. `page_end`, the last **pdf page numbered** page students should read

None values are permitted in the `chapter`, `page_start`, and `page_end` columns, but nowhere else. A missing value in `page_start` will be filled with `0`, while a missing value in `page_end` will be filled with the last page of the resource. Thus, the following entry:

Week | Date | Topic | Reference | Chapter | page_start | page_end
-----|------|-------|-----------|---------|------------|---------
1|4-Oct|Consumption, Savings, Balance of Payments|GLS| None    | None       |None

Would assign the entire "GLS" reference for students. This can be mixed-and-matched; see the example in `materials/lesson_plan.csv` for a full example

## Reference to File mapping
Another file you need to provide is a mapping from bibtex reference IDs to PDF filenames. This should be a sample YAML file. Here is the mapping from the example in `materials/ref_to_file.yaml`:

```yaml
GLS: GLS_Inter...
U: uribe-notes.pdf
S1: rbc_notes...
S2: stylized_...
SE: rbc_exten...
```

The `...` is a flag for the script to auto-complete. You only need to provide as much of the PDF as is necessary to get a unique match, but you can also provide the entire filename if you like.

## Bibtex

The required bibtex is a normal bibtex object. The only requirements are that:

1. All IDs declared in the bibtex file are used in the lesson plan
2. No unused bibtex entries are present
