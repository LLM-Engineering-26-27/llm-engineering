"""Tests for the supplied raw token windows and the single shift."""

from __future__ import annotations

import numpy as np
import pytest
import torch

from llm_engineering.data.dataset import TokenWindows, shift_window


def _write_shard(path, tokens, dtype=np.uint16):
    np.save(path, np.asarray(tokens, dtype=dtype))
    return path


def test_token_windows_counts_and_returns_contiguous_int64_windows(tmp_path):
    path = _write_shard(tmp_path / "tokens.npy", range(100))
    windows = TokenWindows(path, sequence_length=9, vocab_size=100)

    assert len(windows) == 10
    first = windows[0]
    assert first.shape == (10,)
    assert first.dtype == torch.int64
    assert first.tolist() == list(range(10))
    assert windows[1].tolist() == list(range(10, 20))


def test_a_partial_trailing_window_is_not_counted(tmp_path):
    path = _write_shard(tmp_path / "tokens.npy", range(105))
    assert len(TokenWindows(path, sequence_length=9, vocab_size=200)) == 10


def test_shift_window_aligns_inputs_with_next_token_labels():
    raw = torch.arange(12).reshape(2, 6)
    inputs, labels = shift_window(raw)

    assert inputs.shape == (2, 5)
    assert labels.shape == (2, 5)
    assert torch.equal(inputs, raw[:, :-1])
    assert torch.equal(labels, raw[:, 1:])
    assert torch.equal(inputs[:, 1:], labels[:, :-1])


def test_a_non_uint16_shard_names_the_expected_dtype(tmp_path):
    path = _write_shard(tmp_path / "tokens.npy", range(100), dtype=np.int32)
    with pytest.raises(ValueError, match="uint16"):
        TokenWindows(path, sequence_length=9, vocab_size=100)


def test_a_two_dimensional_shard_names_the_expected_rank(tmp_path):
    np.save(tmp_path / "tokens.npy", np.zeros((4, 4), dtype=np.uint16))
    with pytest.raises(ValueError, match="1-D"):
        TokenWindows(tmp_path / "tokens.npy", sequence_length=2, vocab_size=8)


def test_a_shard_shorter_than_one_window_names_the_required_length(tmp_path):
    path = _write_shard(tmp_path / "tokens.npy", range(5))
    with pytest.raises(ValueError, match="sequence_length \\+ 1 = 10"):
        TokenWindows(path, sequence_length=9, vocab_size=100)


def test_a_token_id_at_or_above_vocab_size_names_the_configured_vocab(tmp_path):
    path = _write_shard(tmp_path / "tokens.npy", range(100))
    with pytest.raises(ValueError, match="vocab_size is 50"):
        TokenWindows(path, sequence_length=9, vocab_size=50)
