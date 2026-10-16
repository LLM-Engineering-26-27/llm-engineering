# LLM Engineering

This is the course framework for LLM Engineering: a training codebase you extend week by
week, starting from a one-head, one-block transformer and growing it into a
production-style pretraining and post-training pipeline. Each week you implement a
scaffolded piece of `src/llm_engineering/` against its instructions and a public test suite,
on top of the course's reference solution to the previous week.

## Install

```
pip install -e ".[dev]"
```

## Run the tests

```
pytest tests/ -m "not external_artifact"
```

The public tests are feedback while you work, not your grade: grading runs a separate
hidden suite against your submission.

Before you push a `submit/wNN` branch, check the submission the way the grader rebuilds it:

```
scripts/run.sh test
```

Each week you work on an `attempt/wNN` branch that starts at that week's starter, the tagged
commit `starter/wNN/vM` the course gives you. To hand the week in, you move a `submit/wNN`
branch to the commit you submit. The week's instructions, `exercises/week-NN/README.md`, list
the files you submit and when to move that branch.

`run.sh test` runs `scripts/check_submission.sh` as a batch job on the cluster's CPU queue. It
waits until the job ends, which includes any time in the queue and is usually a few minutes,
then prints the job's log and exits 0 on a pass and 1 otherwise. The log stays in
`logs/lme-job-<job id>.out`. If you stop waiting with Ctrl-C, the job keeps running.

The check takes the starter, adds only the files you submit, as they are committed, and runs
the starter's public tests. It fails on a committed change to any other file, a public test or
a config for example, because the grader does not accept such changes. Uncommitted work is not
checked, so `git add` and `git commit` first. Once it has found your files, the check also lists
any of them that still has uncommitted changes. The same check runs on GitHub each time you push a `submit/wNN` branch,
and a pass there means the same as a pass on the cluster. On a laptop, after
`pip install -e ".[dev]"`, `bash scripts/check_submission.sh` runs it directly.

## Train

Both commands below must be run from the repository root, because config paths (for
example `data.tokens_path`) and the `--config` flag are resolved relative to the current
working directory.

A ten-step CPU smoke run, useful to check your changes run at all before submitting a job:

```
python scripts/train.py --config configs/debug.yaml
```

The graded run, submitted to the cluster once `scripts/run.sh setup` has run there (see
Cluster below):

```
scripts/run.sh train configs/week-02.yaml
```

## Cluster

Graded GPU work and the submission check run as batch jobs on bwUniCluster 3.0. The tests and
the CPU smoke runs are fine on your laptop while you work, but the cluster is the reference.
Once, follow [CLUSTER.md](CLUSTER.md): it takes you from registering for bwUniCluster 3.0 to
a workspace (`ws_allocate lme 60`, renewed with `ws_extend lme 60` before it expires), a clone
of your pair's repository inside it (`cd "$(ws_find lme)"`), and a first GPU job. Its last part
runs, from the repository root and still on the login node:

```
scripts/run.sh setup
```

`setup` links the full training shard from the course directory into `assets/`. Running it
again is harmless. It needs read access to the course directory: if it prints `cannot read`,
send the course staff your cluster username. After that:

- `scripts/run.sh train <config.yaml> [sbatch flags]` submits a training run. Its flags go
  after the config.
- `scripts/run.sh job [sbatch flags] -- <command>` submits any command, for example
  `scripts/run.sh job -- python scripts/train.py --config configs/week-02.yaml`, which is what
  `train` submits.
  Its sbatch flags go before the `--`.
- `scripts/run.sh interactive` opens a shell on a GPU node, for debugging only.
- `scripts/run.sh test [sbatch flags]` runs the submission check (see Run the tests) on a CPU
  node and waits for its result.

There are two GPU queues, both with an NVIDIA H100. `gpu_h100_short` allows 30 minutes and is
the default. `gpu_h100` is for longer runs, and each week's instructions name the commands that
need it and give the flags (`--partition=gpu_h100 --time=01:30:00`). Each job writes its log
to `logs/lme-job-<job id>.out`, and `tail -f` on that file follows a running job. `squeue --me`
lists your jobs, and `scancel <job id>` stops one. A job that hits its time limit ends as
`TIMEOUT` in `sacct -j <job id>`. Submit it again with a longer `--time`, on `gpu_h100` if it
needs more than 30 minutes. Install nothing on the cluster: the job runs in a container image
that carries the environment, and `pip install -e ".[dev]"` is for your laptop.

Your results are produced in the cluster clone. Commit and push them from there (add an SSH
key on the cluster to your GitHub account), or copy the `evidence/` directory to your laptop
with `rsync` and commit it there.

## Where outputs and data live

Each run writes to `runs/<run_name>/`: `config.yaml` (the resolved config),
`metrics.jsonl` (one JSON object per logged step), `checkpoint.pt`, and `loss.png`. This
directory is gitignored — it is scratch space, not something you commit. The evidence you
do commit for a graded week lives under `evidence/week-NN/`.

Training data comes from two pre-tokenized token shards under `assets/`:
`assets/synth_monad_v1.npy` is the full course shard, which `scripts/run.sh setup` links on the cluster, and
`assets/synth_monad_mini_v1.npy` is the small shard committed to the repository that
`configs/debug.yaml` uses for the CPU smoke run. `assets/synth_monad_v1.provenance.json`
records how the full shard was built.
