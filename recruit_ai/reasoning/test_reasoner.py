from pathlib import Path

from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.reasoning.llm_reasoner import generate_report

resume = extract_text(
    "data/raw/resumes/resume1.pdf"
)

job = Path(
    "data/raw/jobs/job1.txt"
).read_text()

print(
    generate_report(
        resume,
        job,
    )
)