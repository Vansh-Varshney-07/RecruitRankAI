from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.parser import parse_resume
from recruit_ai.job.parser import parse_job

from recruit_ai.ranking.hybrid_matcher import hybrid_skill_score


resume = extract_text(
    "data/raw/resumes/resume1.pdf"
)

candidate = parse_resume(resume)

job = """
Machine Learning Engineer

REQUIRED SKILLS

Python
Machine Learning
Git
Docker
Linux
"""

job_profile = parse_job(job)

score = hybrid_skill_score(
    candidate,
    job_profile,
)

print()

print("=" * 40)
print("Hybrid Skill Score")
print("=" * 40)

print(score)