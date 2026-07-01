# RecruitRankAI

RecruitRankAI is a signal-first candidate ranking system built for the India Runs / Redrob hiring-intelligence challenge. It goes beyond keyword filters by combining structured profile parsing, semantic skill fit, behavioral/career signals, and an optional local LLM judge that explains and adjusts shortlist decisions.

## Competition Fit

The challenge asks for:

- Deep job understanding
- Contextual relevance beyond keywords
- Signal integration across profile, career metadata, and behavioral activity
- A fast ranked shortlist in the required output format

RecruitRankAI maps directly to those goals:

- `recruit_ai/job`: parses messy TXT/PDF job descriptions with aliases such as required qualifications, nice-to-have skills, work experience, and responsibilities.
- `recruit_ai/redrob`: streams the large JSONL candidate dataset and converts it into a consistent candidate domain model.
- `recruit_ai/ranking`: produces fast deterministic rankings using exact skills, semantic similarity, experience, education, and project signals.
- `recruit_ai/reasoning/recruiter_brain.py`: optionally uses local Ollama/Qwen as a senior recruiter judge for shortlist-level review, red flags, interview probes, and small score adjustments.
- `recruit_ai/submission`: generates the required `candidate_id,rank,score,reasoning` CSV.

## Core Idea

The system is designed as a two-stage ranking engine:

1. **Fast retrieval/ranking layer** scores thousands of candidates deterministically.
2. **LLM recruiter brain** reviews only the shortlist, where deeper contextual reasoning matters most and latency stays practical.

This makes the project demo-friendly, scalable, and explainable.

## Features

- TXT and PDF job-description upload
- Real Redrob JSONL candidate ingestion
- Robust job section parsing with bullet/comma/semicolon support
- Weighted ranking across skill, semantic, experience, education, and project signals
- Searchable results by name, skill, headline, or location
- Recruiter-facing candidate explanations
- Optional LLM review with deterministic fallback if Ollama is offline
- CSV export from the dashboard
- Hackathon submission CSV generator
- Dark premium Streamlit dashboard

## Run

```bash
uv sync
uv run streamlit run app.py --server.port 8501
```

Open:

```text
http://127.0.0.1:8501
```

## Optional LLM Setup

Install and run Ollama, then pull a local model:

```bash
ollama pull qwen2.5-coder:7b-instruct
```

In the UI, enable **LLM Recruiter Brain**. If Ollama is unavailable, RecruitRankAI automatically falls back to deterministic explanations.

## Generate Submission CSV

Quick sample run:

```bash
uv run python -m recruit_ai.submission.generate_submission --scan-limit 5000
```

Full dataset run:

```bash
uv run python -m recruit_ai.submission.generate_submission
```

Default output:

```text
data/output/recruitrankai_submission.csv
```

## Test

```bash
uv run pytest -q tests
```

## Architecture

```text
Job TXT/PDF
   |
   v
Job Parser -> structured requirements
   |
   v
Redrob JSONL -> CandidateProfile model
   |
   v
Deterministic ranker -> weighted shortlist
   |
   +--> Dashboard explanations/export
   |
   v
Optional LLM recruiter brain -> nuanced review, risks, probes, score delta
   |
   v
Submission CSV
```

## Deploy

Production-ready deployment files are included:

- `Dockerfile.api` for the FastAPI backend
- `render.yaml` for Render free-tier deployment
- `frontend/` for Vercel static deployment
- `.github/workflows/ci.yml` for CI
- `.env.example` for environment variables

See [DEPLOYMENT.md](DEPLOYMENT.md) and [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md).

## Tech Stack

- Python 3.12
- Streamlit
- pandas / Plotly
- PyMuPDF
- Ollama
- Qwen2.5-Coder
- ChromaDB-ready storage modules
- uv
