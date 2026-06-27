from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.parser import parse_resume


profile = parse_resume(
    extract_text(
        "data/raw/resumes/resume1.pdf"
    )
)

print()

print("=" * 50)

print("PROJECTS")

print("=" * 50)

for project in profile.projects:

    print()

    print(project.title)

    print()

    print(project.description)