from recruit_ai.ingestion.pdf_loader import extract_text

from recruit_ai.candidate.parser import parse_resume

from recruit_ai.job.parser import parse_job

from recruit_ai.ranking.scorer import overall_score


resume = extract_text(
    "data/raw/resumes/resume1.pdf"
)

candidate = parse_resume(resume)


job = """
Machine Learning Engineer

REQUIRED SKILLS

Python
Machine Learning
SQL
Git
Docker
"""

job_profile = parse_job(job)

scores = overall_score(
    candidate,
    job_profile,
)

print()

print("=" * 40)

print("RecruitRankAI Score")

print("=" * 40)

for key, value in scores.items():

    print(f"{key:15}: {value:.3f}")