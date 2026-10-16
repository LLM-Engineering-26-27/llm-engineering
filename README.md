# LLM Engineering

This is the course framework for LLM Engineering (University of Tübingen, winter 2026/27): a
training codebase you extend week by week, starting from a one-head, one-block transformer and
growing it into a production-style pretraining and post-training pipeline. The lectures are at
[llm.strueber.dev](https://llm.strueber.dev).

This repository holds the framework as it stands before the first exercise. Anyone may read it,
clone it and run its tests.

**If you take the course**, use this repository to get set up now:

1. Follow [CLUSTER.md](CLUSTER.md). Start Part A today, because registration takes days.
   Part D clones this repository onto the cluster.
2. After the first tutorial in Week 2, you get your pair's repository in the course
   organization. Your graded work happens there, not here. It starts from the same code plus
   the Week 2 exercise, and you clone it the same way (CLUSTER.md, Part D).

## What is where

```
src/llm_engineering/      the package you extend all semester
  data/dataset.py         TokenWindows: the pre-tokenized shard as fixed-length windows;
                          shift_window: inputs and next-token labels
  data/tokenizer.py       loads the pinned course tokenizer
  utils/config.py         the typed config: YAML in, dataclasses out, one fingerprint
  utils/checkpoint.py     atomic checkpoint writes
  utils/logging.py        the run record, one JSON object per line
  utils/plotting.py       loss curves
  utils/rng.py            one call that seeds Python, NumPy and torch
  model/, training/, ...  empty for now: the exercises fill them, starting in Week 2
configs/                  one YAML file per run (see Configs below)
tests/                    public tests, mirroring src/
scripts/run.sh            every cluster job goes through this (see Cluster below)
scripts/slurm/            the batch job and the cluster settings behind run.sh
scripts/check_submission.sh
                          the submission check, used from Week 2 on
assets/                   the small training shard and the full shard's provenance
CLUSTER.md                from no account to a first GPU job on bwUniCluster 3.0
```

Start reading with `utils/config.py` and `data/dataset.py`: every exercise takes its sizes from
the config, and the dataset is where token IDs come from.

## Install and run the tests

On your laptop, from the repository root:

```
pip install -e ".[dev]"
pytest tests/ -m "not external_artifact"
```

All tests pass on this code. They cover the provided infrastructure. Each week's exercise adds
public tests for the parts you write. Grading runs a separate hidden suite against your
submission, which is not part of any course repository.

## Configs

Every hyperparameter a run needs lives in a YAML file under `configs/`, and `load_config` turns
it into typed dataclasses. It rejects unknown keys, so a typo fails at load time, not after an
hour of training.

- `configs/debug.yaml`: a tiny model on the small shard `assets/synth_monad_mini_v1.npy`, for a
  ten-step CPU run that checks your code runs at all.
- `configs/week-02.yaml`: the first graded run.
- `configs/base.yaml`: the depth-eight model that later weeks build on.

## Cluster

Graded GPU work runs as batch jobs on bwUniCluster 3.0. [CLUSTER.md](CLUSTER.md) takes you
there once: registration, login, a workspace (`ws_allocate lme 60`), a first GPU job, a clone
of the repository in the workspace, and then, from the repository root on the login node:

```
scripts/run.sh setup
```

`setup` links the full training shard from the course directory into `assets/`. It needs read
access to the course directory: if it prints `cannot read`, send the course staff your cluster
username. After that:

- `scripts/run.sh job [sbatch flags] -- <command>` submits any command as a batch job.
- `scripts/run.sh interactive` opens a shell on a GPU node, for debugging only.
- From Week 2 on, `scripts/run.sh train <config.yaml>` submits a training run, and
  `scripts/run.sh test` runs the submission check. Both need files that arrive with the
  Week 2 exercise in your pair's repository.

Each job writes its log to `logs/lme-job-<job id>.out`. `squeue --me` lists your jobs, and
`scancel <job id>` stops one. Install nothing on the cluster: jobs run in a container image that
carries the environment, and `pip install -e ".[dev]"` is for your laptop.

## Where outputs and data live

From Week 2 on, each run writes to `runs/<run_name>/`: the resolved config, `metrics.jsonl`,
a checkpoint and a loss plot. That directory is gitignored. The evidence you commit for a
graded week goes under `evidence/week-NN/`.

Training data comes from two pre-tokenized shards. `assets/synth_monad_mini_v1.npy` is the
small shard in this repository. `assets/synth_monad_v1.npy` is the full course shard, which
`scripts/run.sh setup` links on the cluster. `assets/synth_monad_v1.provenance.json` records how
it was built.

## License

The code is released under the MIT License (see [LICENSE](LICENSE)). The token shards in
`assets/` are derived from [PleIAs SYNTH](https://huggingface.co/datasets/PleIAs/SYNTH), which
is licensed under CC-BY-4.0, and keep that license. `assets/synth_monad_v1.provenance.json`
records how they were built.
