from pathlib import Path

from recruit_ai.job.parser import parse_job
from recruit_ai.job.job_graph import build_job_graph

job_path = Path("data/raw/jobs/job1.txt")

text = job_path.read_text(encoding="utf-8")

job = parse_job(text)

graph = build_job_graph(job)

print("\nNodes")
print("=" * 40)

for node in graph.nodes:
    print(node)

print("\nEdges")
print("=" * 40)

for edge in graph.edges:
    print(edge)