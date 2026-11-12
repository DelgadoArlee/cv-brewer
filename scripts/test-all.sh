#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

overall_status=0

for script in test-features.sh test-processes.sh test-systems.sh test-e2e.sh; do
    echo "Running ${script}..."
    status=0
    "./scripts/${script}" "$@" || status=$?

    if [[ "${status}" -eq 5 ]]; then
        echo "No tests collected by ${script}."
    elif [[ "${status}" -ne 0 ]]; then
        echo "${script} failed with exit code ${status}." >&2
        overall_status="${status}"
    fi
done

exit "${overall_status}"
