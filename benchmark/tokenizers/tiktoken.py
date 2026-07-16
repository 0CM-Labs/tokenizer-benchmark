"""
tiktoken.py

TikToken tokenizer adapter.
"""

import tiktoken

from benchmark.tokenizers.base import BaseTokenizer


class TikTokenTokenizer(BaseTokenizer):
    """
    Adapter for TikToken encodings.
    """

    def __init__(self, encoding_name: str):
        self._encoding_name = encoding_name
        self._tokenizer = tiktoken.get_encoding(encoding_name)

    def name(self) -> str:
        """
        Return the tokenizer name.
        """
        return self._encoding_name

    def encode(self, text: str) -> list[int]:
        """
        Encode text into token IDs.
        """
        return self._tokenizer.encode(text)
