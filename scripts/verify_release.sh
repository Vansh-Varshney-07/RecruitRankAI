#!/usr/bin/env bash
set -euo pipefail

python -m compileall -q recruit_ai ui app.py tests
export UV_PROJECT_ENVIRONMENT=.venv-release

uv run pytest -q tests
uv run python -m recruit_ai.submission.generate_submission --scan-limit 100 --top-n 10 --output data/output/smoke_submission.csv

echo "RecruitRankAI release verification passed."
