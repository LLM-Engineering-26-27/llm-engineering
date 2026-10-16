"""The run record: one JSON object per line, appended as training proceeds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def append_jsonl(path: str | Path, **fields: Any) -> None:
    """Append one JSON object to `path`, in the keyword order given."""
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(fields) + "\n")


def read_jsonl(path: str | Path) -> list[dict]:
    """Read every record back, in file order."""
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]
