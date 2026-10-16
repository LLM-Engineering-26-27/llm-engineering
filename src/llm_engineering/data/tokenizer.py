"""Loading the pinned course tokenizer."""

from __future__ import annotations

from transformers import AutoTokenizer, PreTrainedTokenizerBase


def load_tokenizer(name: str, revision: str) -> PreTrainedTokenizerBase:
    """Load one immutable tokenizer revision from the Hub, without remote code."""
    return AutoTokenizer.from_pretrained(
        name, revision=revision, trust_remote_code=False
    )
