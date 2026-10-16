#!/usr/bin/env bash
# Check your submission the way the grader rebuilds it: the starter you were given, plus only
# the files you submit, exactly as they are committed, plus the starter's own public tests.
#
#   scripts/run.sh test                  on the cluster, as a batch job (the reference)
#   bash scripts/check_submission.sh     anywhere else, from inside your repository
#
# It exits 0 when every public test passes and 1 otherwise. Only committed work is checked,
# so commit before you run it. The files you submit are listed in the starter's RELEASE.json.

set -euo pipefail

fail() {
    echo "$*" >&2
    exit 1
}

top="$(git rev-parse --show-toplevel 2>/dev/null)" \
    || fail "Run this inside your pair repository, which is a git clone."
cd "${top}"
repo="${PWD}"

# Prints one field of a committed RELEASE.json. A list field prints one entry per line.
field() {
    git show "$1:RELEASE.json" | python -c '
import json, sys
value = json.load(sys.stdin).get(sys.argv[1], "")
print("\n".join(value) if isinstance(value, list) else value)' "$2"
}

git cat-file -e HEAD:RELEASE.json 2>/dev/null \
    || fail "This commit has no RELEASE.json. Run this on a branch that starts from the week's starter tag, such as attempt/wNN or submit/wNN."
[[ "$(field HEAD kind)" == starter ]] \
    || fail "This commit is not on a week's starter. Run this on a branch that starts from the week's starter tag, such as attempt/wNN or submit/wNN."
release="$(field HEAD release_id)"
tag="refs/tags/${release}"
git rev-parse -q --verify "${tag}^{commit}" >/dev/null \
    || fail "The starter tag ${release} is not in this clone. Run git fetch --tags and try again."
[[ "$(field "${tag}" kind)" == starter ]] \
    || fail "The tag ${release} is not a week's starter. Run this on a branch that starts from the week's starter tag, such as attempt/wNN or submit/wNN."
git merge-base --is-ancestor "${tag}" HEAD \
    || fail "This commit does not descend from the starter ${release}. Start your branch from that tag."

# The files you submit, read from the starter's own RELEASE.json, never from yours.
paths=()
while IFS= read -r path; do
    [[ -n "${path}" ]] && paths+=("${path}")
done < <(field "${tag}" student_submission_paths)
[[ ${#paths[@]} -gt 0 ]] \
    || fail "The starter ${release} lists no files to submit. Send the course staff that release name."

submitted() {
    local path
    for path in "${paths[@]}"; do
        [[ "$1" == "${path}" ]] && return 0
    done
    return 1
}

uncommitted="$(git status --porcelain -- "${paths[@]}" | cut -c4-)"
note_uncommitted() {
    [[ -z "${uncommitted}" ]] && return 0
    echo "Not checked: these files have changes you have not committed. Commit them to include them:"
    echo "${uncommitted}" | sed 's/^/  /'
}

# Every other file must be exactly as the starter has it.
outside=()
while IFS=$'\t' read -r status path; do
    submitted "${path}" && continue
    if [[ "${status}" == A ]]; then
        outside+=("${path}   (you added it: git rm ${path})")
    else
        outside+=("${path}   (restore it: git checkout ${release} -- ${path})")
    fi
done < <(git diff --no-renames --name-status "${tag}" HEAD)
if [[ ${#outside[@]} -gt 0 ]]; then
    note_uncommitted
    printf '  %s\n' "${outside[@]}" >&2
    fail "You committed changes to files you do not submit, listed above. The grader does not accept them, so undo each one as shown, then git commit and run the check again."
fi

while read -r mode _ _ path; do
    [[ "${mode}" == 100644 || "${mode}" == 100755 ]] \
        || fail "${path} must be a regular file, not a symbolic link or a submodule."
done < <(git ls-tree -r HEAD -- "${paths[@]}")

# After the checks above, the committed tree is the starter plus your submitted files.
tree="$(mktemp -d)"
trap 'rm -rf "${tree}"' EXIT
git archive HEAD | tar -x -C "${tree}"

# Tests that start a child Python process must import the rebuilt tree, not this checkout.
checkout_src="$(cd "${repo}/src" 2>/dev/null && pwd -P || echo "${repo}/src")"
pythonpath="${tree}/src"
IFS=: read -r -a entries <<< "${PYTHONPATH:-}"
for entry in ${entries[@]+"${entries[@]}"}; do
    [[ -z "${entry}" || "$(cd "${entry}" 2>/dev/null && pwd -P)" == "${checkout_src}" ]] \
        || pythonpath+=":${entry}"
done
export PYTHONPATH="${pythonpath}"

cd "${tree}"
status=0
python -m pytest tests -q -p no:cacheprovider || status=$?

note_uncommitted
case "${status}" in
    0) echo "Every public test passes on your committed submission." ;;
    1) fail "Your committed submission fails some public tests. The failures are listed above." ;;
    *) fail "The public tests could not run (pytest exit ${status}). Fix the error the output above names, commit, and run the check again." ;;
esac
