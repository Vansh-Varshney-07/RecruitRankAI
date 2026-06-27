from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.parser import parse_resume


text = extract_text(
    "data/raw/resumes/resume1.pdf"
)

profile = parse_resume(text)

print(profile)