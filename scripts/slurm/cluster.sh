# Where the course runs. scripts/run.sh and scripts/slurm/job.sh read these values. No other
# script names a partition, the image, or a path outside the repository, so moving the course
# to another cluster means editing this file.

# The shared, read-only course directory: the image, its extra Python packages, and the full
# training shard.
COURSE_DIR=/pfs/work9/workspace/scratch/tu_iiojo01-lme-course
IMAGE="${COURSE_DIR}/pytorch-26.07-py3.sif"
PYLIBS="${COURSE_DIR}/pylibs/lib/python3.12/site-packages"
SHARD="${COURSE_DIR}/assets/synth_monad_v1.npy"

# Every job starts from these sbatch flags. Flags you give run.sh come after them, and sbatch
# keeps the last value of a repeated flag, so yours win.
SBATCH_DEFAULTS=(--partition=gpu_h100_short --gres=gpu:1 --time=00:30:00)

# `scripts/run.sh test` starts from these instead: the submission check needs no GPU, so it
# runs on the CPU queue, where jobs start sooner.
TEST_SBATCH_DEFAULTS=(--partition=cpu --cpus-per-task=4 --time=00:30:00)

# Run a command inside the image. The image brings Python and PyTorch; PYTHONPATH adds your
# src/ and the packages the image lacks; PYTHONNOUSERSITE keeps packages you may have
# installed in ~/.local from shadowing the image's; LIBRARY_PATH replaces the image's value,
# whose empty last entry makes the C compiler that torch.compile calls also search the current
# directory, where a file or directory named `specs` breaks it; TRITON_LIBCUDA_PATH tells
# torch.compile where the GPU driver library is mounted inside the container. A batch job's
# TMPDIR is a directory on the node that the container cannot see unless it is bound, and
# without it `mktemp` fails inside the container.
in_container() {
    local binds=(--bind "${COURSE_DIR}:${COURSE_DIR}:ro")
    if [[ -n "${TMPDIR:-}" && -d "${TMPDIR}" ]]; then
        binds+=(--bind "${TMPDIR}")
    fi
    apptainer exec --nv "${binds[@]}" \
        --env "PYTHONPATH=${PWD}/src:${PYLIBS}" \
        --env PYTHONNOUSERSITE=1 \
        --env LIBRARY_PATH=/usr/local/cuda/lib64/stubs \
        --env TRITON_LIBCUDA_PATH=/.singularity.d/libs \
        "${IMAGE}" "$@"
}
