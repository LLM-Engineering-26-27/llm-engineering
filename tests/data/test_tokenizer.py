"""Tests for the course tokenizer boundary."""

from __future__ import annotations

import importlib
from unittest.mock import Mock, patch


def test_load_tokenizer_propagates_the_immutable_revision_and_disables_remote_code():
    module = importlib.import_module("llm_engineering.data.tokenizer")
    expected = Mock(name="tokenizer")

    with patch.object(module.AutoTokenizer, "from_pretrained", return_value=expected) as load:
        actual = module.load_tokenizer("example/tokenizer", "immutable-revision")

    assert actual is expected
    load.assert_called_once_with(
        "example/tokenizer",
        revision="immutable-revision",
        trust_remote_code=False,
    )
