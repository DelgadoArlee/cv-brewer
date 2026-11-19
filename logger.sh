#!/usr/bin/env bash
set -euo pipefail

uv run python logger_main.py "$@"
