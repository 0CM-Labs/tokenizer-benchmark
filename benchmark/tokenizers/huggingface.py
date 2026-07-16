"""
huggingface.py

Hugging Face tokenizer adapter.
"""

from transformers import AutoTokenizer

from benchmark.tokenizers.base import BaseTokenizer


class HuggingFaceTokenizer(BaseTokenizer):
    """
    Adapter for Hugging Face tokenizers.
    """

    def __init__(self, config: dict):
        self._config = config

        self._name = config.get("name", config.get("model", "huggingface"))

        self._model = config["model"]

        #
        # Remove benchmark-specific fields.
        #
        tokenizer_kwargs = config.copy()

        tokenizer_kwargs.pop("type", None)
        tokenizer_kwargs.pop("name", None)
        tokenizer_kwargs.pop("model", None)

        self._tokenizer = AutoTokenizer.from_pretrained(self._model, **tokenizer_kwargs)

    def name(self) -> str:
        """
        Return the display name.
        """
        return self._name

    def encode(self, text: str) -> list[int]:
        """
        Encode text into token IDs.
        """

        return self._tokenizer(text, add_special_tokens=False)["input_ids"]
