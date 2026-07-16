"""
tokenizer_factory.py

Creates tokenizer instances from the benchmark configuration.
"""

import tiktoken

from benchmark.config import BenchmarkConfig
from benchmark.tokenizers.tiktoken import TikTokenTokenizer
from benchmark.tokenizers.huggingface import HuggingFaceTokenizer


class TokenizerFactory:
    """
    Factory responsible for creating tokenizer instances.
    """

    def __init__(self, config: BenchmarkConfig):
        self._config = config

    def create(self):
        """
        Create all configured tokenizer instances.

        Returns
        -------
        tuple

            (
                tokenizers,
                errors
            )

        tokenizers : list
            Successfully created tokenizer instances.

        errors : list
            List of tokenizer creation failures.

            Example:

            [
                {
                    "tokenizer": "sarvamai/sarvam-m",
                    "reason": "Network timeout"
                }
            ]
        """

        tokenizers = []
        errors = []

        available_tiktoken = set(tiktoken.list_encoding_names())

        for tokenizer_cfg in self._config.tokenizers:
            #
            # -------------------------------------------------------------
            # TikToken
            # -------------------------------------------------------------
            #
            if isinstance(tokenizer_cfg, str):
                tokenizer_name = tokenizer_cfg

                if tokenizer_name not in available_tiktoken:
                    errors.append(
                        {
                            "tokenizer": tokenizer_name,
                            "reason": "Unknown TikToken encoding.",
                        }
                    )

                    continue

                try:
                    tokenizers.append(TikTokenTokenizer(tokenizer_name))

                except Exception as ex:
                    errors.append({"tokenizer": tokenizer_name, "reason": str(ex)})

                continue

            #
            # -------------------------------------------------------------
            # HuggingFace
            # -------------------------------------------------------------
            #
            if isinstance(tokenizer_cfg, dict):
                tokenizer_name = tokenizer_cfg.get(
                    "name", tokenizer_cfg.get("model", "Unknown")
                )

                tokenizer_type = tokenizer_cfg.get("type")

                if tokenizer_type != "huggingface":
                    errors.append(
                        {
                            "tokenizer": tokenizer_name,
                            "reason": f"Unsupported tokenizer type '{tokenizer_type}'.",
                        }
                    )

                    continue

                try:
                    tokenizers.append(HuggingFaceTokenizer(tokenizer_cfg))

                except Exception as ex:
                    errors.append({"tokenizer": tokenizer_name, "reason": str(ex)})

                continue

            #
            # -------------------------------------------------------------
            # Invalid configuration
            # -------------------------------------------------------------
            #
            errors.append(
                {
                    "tokenizer": str(tokenizer_cfg),
                    "reason": "Invalid tokenizer configuration.",
                }
            )

        return tokenizers, errors
