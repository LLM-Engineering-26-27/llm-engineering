#!/usr/bin/env bash
#SBATCH --job-name=lme-job
#SBATCH --output=logs/%x-%j.out
# Runs one command inside the course image on a cluster node. Submit it through scripts/run.sh,
# which adds the partition, any GPU, and the time limit from scripts/slurm/cluster.sh:
#
#   scripts/run.sh job -- python scripts/train.py --config configs/week-02.yaml

set -euo pipefail

# SLURM runs a copy of this file from its own spool directory, so the repository is found
# through the directory the job was submitted from, which run.sh makes the repository root.
cd "${SLURM_SUBMIT_DIR:?submit this through scripts/run.sh}"
source scripts/slurm/cluster.sh

echo "job ${SLURM_JOB_ID:-?} on $(hostname), commit $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
nvidia-smi -L 2>/dev/null || echo "no GPU on this node"
echo "command: $*"
in_container "$@"
