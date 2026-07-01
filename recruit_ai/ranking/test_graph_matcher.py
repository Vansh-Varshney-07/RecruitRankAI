from pathlib import Path

from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.parser import parse_resume
from recruit_ai.candidate.knowledge_graph import build_graph

from recruit_ai.job.parser import parse_job
from recruit_ai.job.job_graph import build_job_graph

from recruit_ai.ranking.graph_matcher import graph_skill_score


resume_text = extract_text("data/raw/resumes/resume1.pdf")
candidate = parse_resume(resume_text)
candidate_graph = build_graph(candidate)

job_text = Path("data/raw/jobs/job1.txt").read_text(encoding="utf-8")
job = parse_job(job_text)
job_graph = build_job_graph(job)

score = graph_skill_score(candidate_graph, job_graph)

print("\nGraph Skill Score")
print("=" * 40)
print(score)