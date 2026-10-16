"""Tests for the JSONL run record."""

from __future__ import annotations

import json

from llm_engineering.utils.logging import append_jsonl, read_jsonl


def test_append_jsonl_writes_one_line_per_call(tmp_path):
    path = tmp_path / "metrics.jsonl"
    append_jsonl(path, step=1, loss=2.5, lr=0.001)
    append_jsonl(path, step=2, loss=2.0, lr=0.001)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0]) == {"step": 1, "loss": 2.5, "lr": 0.001}


def test_append_jsonl_preserves_the_keyword_order_it_was_called_with(tmp_path):
    path = tmp_path / "metrics.jsonl"
    append_jsonl(path, step=1, loss=2.5, lr=0.001, tokens=64, elapsed_s=0.5)
    assert list(json.loads(path.read_text(encoding="utf-8"))) == [
        "step", "loss", "lr", "tokens", "elapsed_s"
    ]


def test_read_jsonl_returns_every_record_in_order(tmp_path):
    path = tmp_path / "metrics.jsonl"
    for step in range(3):
        append_jsonl(path, step=step)
    assert read_jsonl(path) == [{"step": 0}, {"step": 1}, {"step": 2}]


def test_read_jsonl_of_an_empty_file_is_empty(tmp_path):
    path = tmp_path / "metrics.jsonl"
    path.write_text("", encoding="utf-8")
    assert read_jsonl(path) == []
