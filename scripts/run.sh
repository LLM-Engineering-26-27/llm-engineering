#!/usr/bin/env bash
# Submit course work to the cluster. Run it from anywhere; paths you give it are relative to
# the repository root.
#
#   scripts/run.sh setup                                 once: link the full training shard
#   scripts/run.sh train <config.yaml> [sbatch flags]    a training run, as a batch job
#   scripts/run.sh job [sbatch flags] -- <command...>    any command, as a batch job
#   scripts/run.sh interactive [srun flags]              a shell on a GPU node, for debugging
#   scripts/run.sh test [sbatch flags]                   check your committed submission, as a batch job
#
# Jobs start from the defaults in scripts/slurm/cluster.sh (the 30-minute GPU queue); add
# --partition=gpu_h100 --time=01:30:00 for a run that needs longer. Each job writes its log
# to logs/lme-job-<job id>.out; `squeue --me` lists your jobs.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
source scripts/slurm/cluster.sh

usage() {
    echo "usage: scripts/run.sh setup | train <config.yaml> [sbatch flags] | job [sbatch flags] -- <command...> | interactive [srun flags] | test [sbatch flags]" >&2
    exit 2
}

command="${1:-}"
[[ $# -gt 0 ]] && shift

case "${command}" in
    setup)
        for path in "${IMAGE}" "${SHARD}"; do
            if [[ ! -r "${path}" ]]; then
                echo "cannot read ${path}. Send the course staff your cluster username to get access." >&2
                exit 1
            fi
        done
        ln -sfn "${SHARD}" assets/synth_monad_v1.npy
        echo "assets/synth_monad_v1.npy -> ${SHARD}"
        ;;
    train)
        [[ $# -gt 0 && "$1" != -* ]] || usage
        config="$1"
        shift
        sbatch "${SBATCH_DEFAULTS[@]}" "$@" scripts/slurm/job.sh python scripts/train.py --config "${config}"
        ;;
    job)
        flags=()
        while [[ $# -gt 0 && "$1" != "--" ]]; do
            flags+=("$1")
            shift
        done
        [[ $# -gt 1 ]] || usage
        shift
        sbatch "${SBATCH_DEFAULTS[@]}" ${flags[@]+"${flags[@]}"} scripts/slurm/job.sh "$@"
        ;;
    interactive)
        srun "${SBATCH_DEFAULTS[@]}" "$@" --pty scripts/slurm/job.sh bash
        ;;
    test)
        status=0
        job="$(sbatch --parsable --wait "${TEST_SBATCH_DEFAULTS[@]}" "$@" scripts/slurm/job.sh bash scripts/check_submission.sh)" || status=$?
        job="${job%%;*}"
        [[ -n "${job}" ]] || { echo "The check was not submitted. The sbatch message above says why." >&2; exit 1; }
        cat "logs/lme-job-${job}.out" \
            || echo "Job ${job} wrote no log. Check it with sacct -j ${job}." >&2
        exit "${status}"
        ;;
    *)
        usage
        ;;
esac
