from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.section_parser import split_sections
from recruit_ai.candidate.education_parser import extract_education

text = extract_text(
    "data/raw/resumes/resume1.pdf"
)

sections = split_sections(text)

print(extract_education(sections))