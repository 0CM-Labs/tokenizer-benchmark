"""
runner.py

Coordinates the complete benchmark execution.
"""

from benchmark.config import BenchmarkConfig
from benchmark.dataset_loader import DatasetLoader
from benchmark.tokenizer_factory import TokenizerFactory
from benchmark.report import ReportGenerator
from benchmark.logger import logger


class BenchmarkRunner:
    """
    Coordinates the complete tokenizer benchmark workflow.

    Workflow:

        Load Configuration
                │
                ▼
        Load Dataset
                │
                ▼
        Create Tokenizers
                │
                ▼
        Run Benchmark
                │
                ▼
        Generate Reports
    """

    def __init__(self, config_path: str):
        self._config_path = config_path

    def run(self) -> None:
        """
        Execute the complete benchmark.
        """

        # ------------------------------------------------------------------
        # Load configuration
        # ------------------------------------------------------------------
        logger.info(f"loading benchmark configuration from {self._config_path}")
        config = BenchmarkConfig.load(self._config_path)

        # ------------------------------------------------------------------
        # Load datasets
        # ------------------------------------------------------------------
        dataset_loader = DatasetLoader(config)
        language_datasets = dataset_loader.load()

        # ------------------------------------------------------------------
        # Create tokenizers
        # ------------------------------------------------------------------
        tokenizer_factory = TokenizerFactory(config)
        tokenizers, errors = tokenizer_factory.create()

        # ------------------------------------------------------------------
        # Run benchmark
        # ------------------------------------------------------------------
        results = []

        for tokenizer in tokenizers:
            result = {"Tokenizer": tokenizer.name()}

            for language_name, text in language_datasets.items():
                logger.info(
                    f"test tokenizer {tokenizer.name()} on language {language_name}"
                )
                token_count = len(tokenizer.encode(text))

                result[language_name] = token_count

            results.append(result)

        # ------------------------------------------------------------------
        # Generate reports
        # ------------------------------------------------------------------
        report_generator = ReportGenerator(config)
        logger.info(f"Generate report")
        report_generator.print(results, errors)
        report_generator.write_txt(results, errors)
        report_generator.write_csv(results, errors)
