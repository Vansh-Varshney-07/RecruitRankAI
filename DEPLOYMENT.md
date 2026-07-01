# Deployment Guide

RecruitRankAI has two deployable surfaces:

1. **FastAPI backend** for ranking and candidate intelligence.
2. **Static Vercel frontend** for a public demo.

The Streamlit app remains the local rich demo.

## Backend: Render Free Web Service

The repo includes:

- `Dockerfile.api`
- `render.yaml`
- `Procfile`
- `.env.example`

### Render Blueprint

1. Push this repo to GitHub.
2. Go to Render.
3. Create a new Blueprint from the repository.
4. Render will detect `render.yaml`.
5. Add the candidate dataset to the deployed environment.

Important: `data/redrob/candidates.jsonl` is large and should not be committed to GitHub. For a production backend, upload it as persistent storage or use an object-storage URL and adapt `RECRUITRANKAI_DATASET`.

If the full dataset is absent, the API automatically falls back to `data/redrob/sample_candidates.json` so the deployed demo still works. `/health` reports whether the sample dataset is being used.

Health check:

```text
https://your-api.onrender.com/health
```

Rank endpoint:

```text
POST https://your-api.onrender.com/rank
```

## Frontend: Vercel

Deploy only the `frontend/` folder.

```bash
cd frontend
vercel
```

After deployment, paste your backend URL into the UI.

## Local API

```bash
uv run uvicorn recruit_ai.api.server:app --reload --port 8000
```

Health:

```text
http://127.0.0.1:8000/health
```

Example rank request:

```bash
curl -X POST http://127.0.0.1:8000/rank \
  -H "Content-Type: application/json" \
  -d '{"job_text":"ML Engineer\n\nRequired Skills:\nPython, SQL, Machine Learning","scan_limit":1000,"top_n":10}'
```

## Local Streamlit Demo

```bash
uv run streamlit run app.py --server.port 8501
```

## Submission CSV

```bash
uv run python -m recruit_ai.submission.generate_submission
```

Output:

```text
data/output/recruitrankai_submission.csv
```

## Final Release Verification

Windows:

```powershell
.\scripts\verify_release.ps1
```

Ubuntu / WSL:

```bash
bash scripts/verify_release.sh
```
