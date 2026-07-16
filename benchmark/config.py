"""
config.py

Loads and validates the benchmark configuration.
"""

import json
from pathlib import Path


class BenchmarkConfig:
    """
    Represents the benchmark configuration loaded from JSON.
    """

    REQUIRED_FIELDS = [
        "dataset",
        "languages",
        "tokenizers",
        "output",
    ]

    def __init__(self, config: dict):
        self._config = config

    @classmethod
    def load(cls, config_path: str) -> "BenchmarkConfig":
        """
        Load configuration from a JSON file.
        """

        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        with config_file.open("r", encoding="utf-8") as f:
            config = json.load(f)

        cls._validate(config)

        return cls(config)

    @classmethod
    def _validate(cls, config: dict) -> None:
        """
        Validate the top-level configuration structure.
        """

        for field in cls.REQUIRED_FIELDS:
            if field not in config:
                raise ValueError(f"Missing required field '{field}' in configuration.")

    @property
    def dataset(self) -> str:
        return self._config["dataset"]

    @property
    def languages(self) -> list[str]:
        return self._config["languages"]

    @property
    def tokenizers(self) -> list:
        return self._config["tokenizers"]

    @property
    def output(self) -> dict:
        return self._config["output"]
