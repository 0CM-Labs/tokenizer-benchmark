"""
logger.py

Central logging utility for the benchmark project.
"""

import logging
import sys


class _FunctionNameFilter(logging.Filter):
    """
    Replaces %(funcName)s with ClassName.functionName when available.
    """

    def filter(self, record):
        if hasattr(record, "classname"):
            record.funcName = f"{record.classname}.{record.funcName}"
        return True


def _create_logger() -> logging.Logger:

    logger = logging.getLogger("TokenizerBenchmark")

    #
    # Avoid duplicate handlers if imported multiple times.
    #
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(funcName)-35s | %(message)s",
        datefmt="%H:%M:%S",
    )

    handler.setFormatter(formatter)
    handler.addFilter(_FunctionNameFilter())

    logger.addHandler(handler)

    return logger


logger = _create_logger()
