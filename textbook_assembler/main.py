import argparse
import logging

_log = logging.getLogger("textbook_assembler")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        required=False,
        default="config/input_data.csv",
        help="Path to the CSV file containing output content",
    )
    parser.add_argument(
        "--source_dir",
        "-s",
        type=str,
        required=False,
        default="sources/",
        help="Path to directory containing PDFs to be assembled",
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        required=False,
        default="/",
        help="Path to output directory for assembled textbook",
    )
    parser.add_argument(
        "--latex_config",
        "-lc",
        type=str,
        required=False,
        default=None,
        help="Path to directory containing LaTeX configuration for cover pages",
    )
    parser.add_argument(
        "--ref_to_path",
        "-rp",
        type=str,
        required=False,
        default=None,
        help="Path to YAML with mapping between bibtex references and source files",
    )

    args = parser.parse_args()


if __name__ == "__main__":
    main()
