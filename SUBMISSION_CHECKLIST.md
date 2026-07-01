# Submission Checklist

## Required

- [ ] GitHub repository is public or shared with judges.
- [ ] README explains methodology, architecture, and technical choices.
- [ ] Ranked CSV follows `candidate_id,rank,score,reasoning`.
- [ ] Dataset path is documented and not accidentally missing during demo.
- [ ] Streamlit local demo works.
- [ ] API `/health` works.
- [ ] API `/rank` works.
- [ ] Tests pass.
- [ ] `scripts/verify_release.ps1` or `scripts/verify_release.sh` passes.
- [ ] Full `data/redrob/candidates.jsonl` is available locally before generating final submission.
- [ ] Hosted API `/health` does not show sample dataset when presenting final scoring claims.

## Recommended Demo Flow

1. Open Streamlit app.
2. Upload the challenge job description as TXT/PDF.
3. Run deterministic ranking.
4. Enable **LLM Recruiter Brain** for top shortlist.
5. Show candidate cards: score, reasons, missing skills, interview probes.
6. Download ranked CSV.
7. Show `data/output/recruitrankai_submission.csv`.

## Final Commands

```bash
uv sync --dev
uv run pytest -q tests
uv run python -m recruit_ai.submission.generate_submission
uv run streamlit run app.py --server.port 8501
```
