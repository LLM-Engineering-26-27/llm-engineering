"""Tests for the course configuration boundary."""

from __future__ import annotations

import re

import pytest

from llm_engineering.utils.config import (
    ModelConfig,
    config_fingerprint,
    load_config,
    save_config,
)


CONFIG_NAMES = ("base.yaml", "debug.yaml", "week-02.yaml")


@pytest.mark.parametrize("name", CONFIG_NAMES)
def test_every_shipped_config_round_trips_through_save_and_load(name, configs_dir, tmp_path):
    original = load_config(configs_dir / name)
    copied = tmp_path / name
    save_config(original, copied)
    assert load_config(copied) == original
    assert config_fingerprint(load_config(copied)) == config_fingerprint(original)


def test_model_defaults_resolve_d_ff_and_n_kv_heads():
    model = ModelConfig()
    assert model.d_ff == 3 * model.d_model
    assert model.n_kv_heads == model.n_heads


def test_an_unknown_top_level_key_names_the_key_and_the_allowed_keys(tmp_path):
    path = tmp_path / "unknown.yaml"
    path.write_text("schema_version: 1\n", encoding="utf-8")
    with pytest.raises(ValueError) as failure:
        load_config(path)
    message = str(failure.value)
    assert "schema_version" in message
    assert "run_name" in message


def test_an_unknown_section_key_is_rejected(tmp_path):
    path = tmp_path / "unknown-section-key.yaml"
    path.write_text("model:\n  dropout: 0.0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="dropout"):
        load_config(path)


@pytest.mark.parametrize(
    ("payload", "expected"),
    (
        ("model:\n  d_model: 0\n", "model.d_model must be at least 1; got 0"),
        ("model:\n  d_model: 12\n  n_heads: 5\n", "must be divisible by"),
        (
            "model:\n  max_context_length: 16\ndata:\n  sequence_length: 32\n",
            "data.sequence_length (32) must not exceed model.max_context_length (16)",
        ),
        (
            "training:\n  max_steps: 4\nschedule:\n  warmup_steps: 8\n",
            "schedule.warmup_steps (8) must not exceed training.max_steps (4)",
        ),
    ),
)
def test_each_boundary_invariant_names_the_expected_value(payload, expected, tmp_path):
    path = tmp_path / "invalid.yaml"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(ValueError, match=re.escape(expected)):
        load_config(path)


def test_the_fingerprint_is_stable_across_loads_and_moves_with_any_field(configs_dir):
    first = load_config(configs_dir / "week-02.yaml")
    second = load_config(configs_dir / "week-02.yaml")
    assert config_fingerprint(first) == config_fingerprint(second)
    second.optimizer.lr = 1e-4
    assert config_fingerprint(first) != config_fingerprint(second)
