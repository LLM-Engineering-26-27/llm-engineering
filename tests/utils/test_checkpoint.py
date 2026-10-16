"""Tests for the atomic checkpoint write."""

from __future__ import annotations

import torch

from llm_engineering.utils.checkpoint import save_checkpoint


def test_save_checkpoint_writes_a_loadable_file_and_leaves_no_temporary(tmp_path):
    path = tmp_path / "checkpoint.pt"
    save_checkpoint({"step": 3, "weight": torch.ones(2)}, path)

    state = torch.load(path, weights_only=True)
    assert state["step"] == 3
    assert torch.equal(state["weight"], torch.ones(2))
    assert list(tmp_path.iterdir()) == [path]


def test_save_checkpoint_replaces_an_existing_file(tmp_path):
    path = tmp_path / "checkpoint.pt"
    save_checkpoint({"step": 1}, path)
    save_checkpoint({"step": 2}, path)
    assert torch.load(path, weights_only=True)["step"] == 2
