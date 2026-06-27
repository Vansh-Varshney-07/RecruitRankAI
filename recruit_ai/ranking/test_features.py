from recruit_ai.ingestion.pdf_loader import extract_text

from recruit_ai.candidate.parser import parse_resume
from recruit_ai.job.parser import parse_job

from recruit_ai.ranking.feature_builder import build_candidate_features
from recruit_ai.ranking.job_features import build_job_features


resume = extract_text("data/raw/resumes/resume1.pdf")

candidate = parse_resume(resume)

job = """
Machine Learning Engineer

REQUIRED SKILLS

Python
Machine Learning
SQL

PREFERRED SKILLS

Docker
Linux

EDUCATION

B.Tech
"""

job_profile = parse_job(job)

print(build_candidate_features(candidate))

print()

print(build_job_features(job_profile))