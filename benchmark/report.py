"""
report.py

Generates benchmark reports.
"""

from pathlib import Path
import csv
from pathlib import Path

from benchmark.config import BenchmarkConfig


class ReportGenerator:
    def __init__(self, config: BenchmarkConfig):
        self._config = config

        self._output_dir = Path(config.output["directory"])
        self._output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Console
    # ---------------------------------------------------------

    def print(self, results: list, errors: list):

        if not self._config.output["console"]:
            return

        self._print_table(results)

        if errors:
            self._print_errors(errors)

    # ---------------------------------------------------------
    # TXT
    # ---------------------------------------------------------

    def write_txt(self, results: list, errors: list):

        if not self._config.output["txt"]:
            return

        dataset_name = self._config.dataset
        output_file = Path(self._output_dir) / f"{dataset_name}_benchmark.txt"

        with output_file.open("w", encoding="utf-8") as f:
            self._write_table(results, f)

            if errors:
                f.write("\n")
                f.write("=" * 80)
                f.write("\n")
                f.write("Tokenizers skipped\n")
                f.write("=" * 80)
                f.write("\n\n")

                for error in errors:
                    f.write(f"{error['tokenizer']}\n")
                    f.write(f"Reason : {error['reason']}\n\n")

    # ---------------------------------------------------------
    # CSV
    # ---------------------------------------------------------

    def write_csv(self, results: list, errors: list):

        if not self._config.output["csv"]:
            return

        dataset_name = self._config.dataset
        output_file = Path(self._output_dir) / f"{dataset_name}_benchmark.csv"

        if not results:
            return

        headers = list(results[0].keys())

        with output_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)

            writer.writeheader()

            for row in results:
                writer.writerow(row)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _print_table(self, results):

        if not results:
            print("No benchmark results.")
            return

        headers = list(results[0].keys())

        widths = {}

        for header in headers:
            widths[header] = max(len(header), max(len(str(r[header])) for r in results))

        #
        # Header
        #
        for header in headers:
            print(f"{header:<{widths[header] + 2}}", end="")

        print()

        #
        # Divider
        #
        for header in headers:
            print("-" * (widths[header] + 2), end="")

        print()

        #
        # Rows
        #
        for row in results:
            for header in headers:
                print(f"{str(row[header]):<{widths[header] + 2}}", end="")

            print()

    def _write_table(self, results, file):

        if not results:
            return

        headers = list(results[0].keys())

        widths = {}

        for header in headers:
            widths[header] = max(len(header), max(len(str(r[header])) for r in results))

        #
        # Header
        #
        for header in headers:
            file.write(f"{header:<{widths[header] + 2}}")

        file.write("\n")

        #
        # Divider
        #
        for header in headers:
            file.write("-" * (widths[header] + 2))

        file.write("\n")

        #
        # Rows
        #
        for row in results:
            for header in headers:
                file.write(f"{str(row[header]):<{widths[header] + 2}}")

            file.write("\n")

    def _print_errors(self, errors):

        print()
        print("=" * 80)
        print("Tokenizers skipped")
        print("=" * 80)

        for error in errors:
            print(f"\n{error['tokenizer']}")
            print(f"Reason : {error['reason']}")
