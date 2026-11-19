#!/usr/bin/env bash
set -euo pipefail

uv run python scripts/query_test_logs.py "$@"
