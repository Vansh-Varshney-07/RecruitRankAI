$ErrorActionPreference = "Stop"

python -m compileall -q recruit_ai ui app.py tests

$env:UV_PROJECT_ENVIRONMENT = ".venv-release"

uv run pytest -q tests
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

uv run python -m recruit_ai.submission.generate_submission --scan-limit 100 --top-n 10 --output data/output/smoke_submission.csv
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "RecruitRankAI release verification passed."
