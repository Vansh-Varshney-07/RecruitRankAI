from pathlib import Path

from recruit_ai.ingestion.pdf_loader import extract_text

from recruit_ai.candidate.parser import parse_resume

from recruit_ai.job.parser import parse_job

from recruit_ai.ranking.rank_candidates import rank_candidates

from recruit_ai.candidate.repository import load_candidates

# ----------------------------
# Load Candidate
# ----------------------------

resume_text = extract_text(
    "data/raw/resumes/resume1.pdf"
)

candidates = load_candidates()

# ----------------------------
# Load Job
# ----------------------------

job_text = Path(
    "data/raw/jobs/job1.txt"
).read_text(encoding="utf-8")

job = parse_job(job_text)


# ----------------------------
# Rank
# ----------------------------

results = rank_candidates(
    candidates,
    job,
)

print()

print("=" * 40)
print("RecruitRankAI Ranking")
print("=" * 40)

for i, item in enumerate(results, start=1):

    print()

    print(f"Rank #{i}")

    print("Candidate :", item["candidate"].name)

    print("Score     :", round(item["score"]["overall"], 3))