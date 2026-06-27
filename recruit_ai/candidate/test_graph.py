from pathlib import Path

from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.parser import parse_resume
from recruit_ai.candidate.knowledge_graph import build_graph


pdf = Path("data/raw/resumes/resume1.pdf")

text = extract_text(str(pdf))

profile = parse_resume(text)

graph = build_graph(profile)

print("\nNodes")
print("=" * 40)

for node in graph.nodes:
    print(node)

print("\nEdges")
print("=" * 40)

for edge in graph.edges:
    print(edge)