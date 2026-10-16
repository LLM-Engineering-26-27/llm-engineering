"""Shared test fixtures for the LLM Engineering test suite."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for CI/headless environments

import pytest

from llm_engineering.utils.config import ModelConfig


@pytest.fixture
def project_root() -> Path:
    """Path to the project root directory."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def configs_dir(project_root) -> Path:
    """Path to the configs/ directory."""
    return project_root / "configs"


@pytest.fixture
def small_model_config() -> ModelConfig:
    """A tiny model config for fast CPU tests."""
    return ModelConfig(d_model=64, vocab_size=100, d_ff=192, max_context_length=64)
