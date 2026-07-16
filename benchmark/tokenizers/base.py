"""
base.py

Defines the common tokenizer interface.

Every tokenizer implementation must inherit from BaseTokenizer.
"""

from abc import ABC, abstractmethod


class BaseTokenizer(ABC):
    """
    Abstract base class for all tokenizer adapters.
    """

    @abstractmethod
    def name(self) -> str:
        """
        Return a human-readable tokenizer name.

        Example
        -------
            gpt2
            o200k_base
            sarvamai/sarvam-m
        """
        pass

    @abstractmethod
    def encode(self, text: str) -> list[int]:
        """
        Tokenize the supplied text.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        list[int]
            List of token IDs.
        """
        pass
