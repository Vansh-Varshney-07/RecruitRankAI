.PHONY: install test compile run-streamlit run-api submission smoke-submission

install:
	uv sync --dev

compile:
	uv run python -m compileall -q recruit_ai ui app.py tests

test:
	uv run pytest -q tests

run-streamlit:
	uv run streamlit run app.py --server.port 8501

run-api:
	uv run uvicorn recruit_ai.api.server:app --reload --port 8000

submission:
	uv run python -m recruit_ai.submission.generate_submission

smoke-submission:
	uv run python -m recruit_ai.submission.generate_submission --scan-limit 5000 --top-n 100 --output data/output/smoke_submission.csv
