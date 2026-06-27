from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.section_parser import split_sections
from recruit_ai.candidate.skill_parser import extract_skills

text = extract_text(
    "data/raw/resumes/resume1.pdf"
)

sections = split_sections(text)

skills = extract_skills(sections)

print()

for skill in skills:
    print(skill)