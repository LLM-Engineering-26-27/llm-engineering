"""Checkpoint writing: a temporary file plus one atomic rename."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import torch


def save_checkpoint(state: dict[str, Any], path: str | Path) -> None:
    """Write `state` to `path` atomically, so a killed job leaves no half file."""
    path = Path(path)
    temporary = path.with_suffix(".tmp")
    torch.save(state, temporary)
    os.replace(temporary, path)
