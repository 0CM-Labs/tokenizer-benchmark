"""
dataset_loader.py

Loads multilingual benchmark datasets.
"""

from pathlib import Path

from benchmark.config import BenchmarkConfig


class DatasetLoader:
    """
    Loads datasets from disk.

    Expected directory structure:

        datasets/
            common1000/
                english.txt
                hindi.txt
                punjabi.txt
    """

    DATASET_ROOT = Path("datasets")

    def __init__(self, config: BenchmarkConfig):
        self._config = config

    def load(self) -> dict[str, str]:
        """
        Load all configured language datasets.

        Returns
        -------
        dict[str, str]

            Example:

            {
                "english": "...",
                "hindi": "...",
                "punjabi": "..."
            }
        """

        dataset_path = self.DATASET_ROOT / self._config.dataset

        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset '{self._config.dataset}' not found.")

        language_data = {}

        for language in self._config.languages:
            file_path = dataset_path / f"{language}.txt"

            if not file_path.exists():
                raise FileNotFoundError(f"Language file not found: {file_path}")

            with file_path.open("r", encoding="utf-8") as f:
                language_data[language] = f.read().strip()

        self._validate_alignment(language_data)

        return language_data

    def _validate_alignment(self, language_data: dict[str, str]) -> None:
        """
        Ensure every language contains the same number of words.
        """

        counts = {
            language: len(text.split()) for language, text in language_data.items()
        }

        expected = next(iter(counts.values()))

        for language, count in counts.items():
            if count != expected:
                raise ValueError(
                    "Language datasets are not aligned.\n"
                    f"Expected {expected} words but "
                    f"'{language}' contains {count}."
                )
