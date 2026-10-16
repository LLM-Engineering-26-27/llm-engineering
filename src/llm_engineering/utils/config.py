"""Typed experiment configuration: YAML in, dataclasses out, one fingerprint.

Every hyperparameter a run needs lives in one of the sections below. `load_config` is the
boundary where a YAML file becomes typed values: it is the only place that rejects an
unknown key or an inconsistent combination, so nothing downstream re-checks them.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
import hashlib
import json
from pathlib import Path
from typing import Any, Literal

import yaml


@dataclass
class ChatTemplateRef:
    """A course-owned chat template pinned by digest. Week 12 reads it."""

    logical_id: str
    locator: str
    sha256: str


@dataclass
class ModelConfig:
    d_model: int = 512
    n_heads: int = 1
    n_kv_heads: int | None = None
    n_layers: int = 1
    vocab_size: int = 8192
    d_ff: int | None = None
    max_context_length: int = 1024
    norm_eps: float = 1e-5
    tie_embeddings: bool = True
    pos_encoding: Literal["sinusoidal", "rope", "nope"] = "sinusoidal"
    rope_theta: float = 10000.0

    def __post_init__(self) -> None:
        if self.d_ff is None:
            self.d_ff = 3 * self.d_model
        if self.n_kv_heads is None:
            self.n_kv_heads = self.n_heads


@dataclass
class DataConfig:
    tokenizer_name: str = "PleIAs/Monad"
    tokenizer_revision: str = "d8fce6b01ee5c5575bf00a74f6e6463ab5796112"
    tokens_path: str = "assets/synth_monad_v1.npy"
    chat_template: ChatTemplateRef | None = None
    sequence_length: int = 1024
    num_workers: int = 0


@dataclass
class TrainingConfig:
    microbatch_size_per_rank: int = 32
    max_steps: int = 1000
    log_interval: int = 10


@dataclass
class OptimizerConfig:
    lr: float = 3e-4
    weight_decay: float = 0.1


@dataclass
class ScheduleConfig:
    warmup_steps: int = 100


@dataclass
class RngConfig:
    seed: int = 42
    deterministic: bool = False


@dataclass
class ExperimentConfig:
    run_name: str = "default"
    model: ModelConfig = field(default_factory=ModelConfig)
    data: DataConfig = field(default_factory=DataConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    optimizer: OptimizerConfig = field(default_factory=OptimizerConfig)
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)
    rng: RngConfig = field(default_factory=RngConfig)


_SECTIONS = {
    "model": ModelConfig,
    "data": DataConfig,
    "training": TrainingConfig,
    "optimizer": OptimizerConfig,
    "schedule": ScheduleConfig,
    "rng": RngConfig,
}
_POSITIVE = (
    ("model.d_model", "model", "d_model"),
    ("model.n_heads", "model", "n_heads"),
    ("model.n_layers", "model", "n_layers"),
    ("model.vocab_size", "model", "vocab_size"),
    ("model.d_ff", "model", "d_ff"),
    ("model.max_context_length", "model", "max_context_length"),
    ("data.sequence_length", "data", "sequence_length"),
    ("training.microbatch_size_per_rank", "training", "microbatch_size_per_rank"),
    ("training.max_steps", "training", "max_steps"),
    ("training.log_interval", "training", "log_interval"),
)


def _build(cls: type, mapping: dict[str, Any], where: str):
    allowed = sorted(entry.name for entry in fields(cls))
    unknown = sorted(set(mapping) - set(allowed))
    if unknown:
        raise ValueError(
            f"{where}: unknown key(s) {unknown}; allowed keys are {allowed}"
        )
    return cls(**mapping)


def load_config(path: str | Path) -> ExperimentConfig:
    """Decode one YAML file into a resolved `ExperimentConfig`."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: the top level must be a mapping of sections")
    sections: dict[str, Any] = {}
    for name, cls in _SECTIONS.items():
        payload = dict(raw.pop(name, {}) or {})
        if name == "data":
            reference = payload.get("chat_template")
            if isinstance(reference, dict):
                payload["chat_template"] = _build(
                    ChatTemplateRef, reference, f"{path}: data.chat_template"
                )
        sections[name] = _build(cls, payload, f"{path}: {name}")
    config = _build(ExperimentConfig, {**raw, **sections}, str(path))
    for label, section, name in _POSITIVE:
        value = getattr(getattr(config, section), name)
        if value < 1:
            raise ValueError(f"{path}: {label} must be at least 1; got {value}")
    if config.model.d_model % config.model.n_heads != 0:
        raise ValueError(
            f"{path}: model.d_model ({config.model.d_model}) must be divisible by "
            f"model.n_heads ({config.model.n_heads})"
        )
    if config.data.sequence_length > config.model.max_context_length:
        raise ValueError(
            f"{path}: data.sequence_length ({config.data.sequence_length}) must not exceed "
            f"model.max_context_length ({config.model.max_context_length})"
        )
    if config.schedule.warmup_steps > config.training.max_steps:
        raise ValueError(
            f"{path}: schedule.warmup_steps ({config.schedule.warmup_steps}) must not "
            f"exceed training.max_steps ({config.training.max_steps})"
        )
    return config


def save_config(config: ExperimentConfig, path: str | Path) -> None:
    """Write the resolved configuration back as YAML, section order preserved."""
    Path(path).write_text(
        yaml.safe_dump(asdict(config), sort_keys=False), encoding="utf-8"
    )


def config_fingerprint(config: ExperimentConfig) -> str:
    """SHA-256 of the resolved configuration: the run's identity in one string."""
    payload = json.dumps(asdict(config), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
