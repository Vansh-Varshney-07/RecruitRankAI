from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.section_parser import split_into_sections

text = extract_text(
    "data/raw/resumes/resume1.pdf"
)

sections = split_into_sections(text)

for name, content in sections.items():

    print("=" * 50)

    print(name.upper())

    print("=" * 50)

    print(content)

    print()