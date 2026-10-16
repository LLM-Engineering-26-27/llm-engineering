"""The supplied token stream: fixed-length windows of raw IDs, and the one shift.

A window is `sequence_length + 1` consecutive token IDs. `shift_window` turns a batch of
windows into the inputs and next-token labels the loss compares, which is the only place in
the course where that shift happens.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch import Tensor


class TokenWindows(torch.utils.data.Dataset):
    """Non-overlapping `[sequence_length + 1]` windows over one flat uint16 token file."""

    def __init__(self, tokens_path: str | Path, sequence_length: int, vocab_size: int):
        self.tokens = np.load(tokens_path, mmap_mode="r")
        self.sequence_length = sequence_length
        if self.tokens.ndim != 1 or self.tokens.dtype != np.uint16:
            raise ValueError(
                f"{tokens_path} must hold a 1-D uint16 array; it holds "
                f"{self.tokens.ndim}-D {self.tokens.dtype}"
            )
        if len(self.tokens) < sequence_length + 1:
            raise ValueError(
                f"{tokens_path} holds {len(self.tokens)} tokens; one window needs "
                f"sequence_length + 1 = {sequence_length + 1}"
            )
        largest = int(self.tokens.max())
        if largest >= vocab_size:
            raise ValueError(
                f"{tokens_path} holds token id {largest}, but the configured "
                f"vocab_size is {vocab_size}, so ids must be below it"
            )

    def __len__(self) -> int:
        return len(self.tokens) // (self.sequence_length + 1)

    def __getitem__(self, index: int) -> Tensor:
        span = self.sequence_length + 1
        start = index * span
        window = self.tokens[start : start + span]
        return torch.from_numpy(window.astype(np.int64))


def shift_window(raw: Tensor) -> tuple[Tensor, Tensor]:
    """Split `[B, S+1]` raw windows into inputs and next-token labels, both `[B, S]`."""
    return raw[:, :-1], raw[:, 1:]
