"""Tests for the seeded RNG setup."""

from __future__ import annotations

import random

import numpy as np
import torch

from llm_engineering.utils.rng import set_seed


def test_set_seed_makes_random_numpy_and_torch_reproducible():
    set_seed(1234)
    first = (random.random(), float(np.random.rand()), float(torch.rand(1)))
    set_seed(1234)
    second = (random.random(), float(np.random.rand()), float(torch.rand(1)))
    assert first == second


def test_set_seed_with_deterministic_enables_torch_deterministic_algorithms():
    try:
        set_seed(0, deterministic=True)
        assert torch.are_deterministic_algorithms_enabled()
    finally:
        torch.use_deterministic_algorithms(False)
