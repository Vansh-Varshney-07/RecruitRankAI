from pathlib import Path

from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.candidate.parser import parse_resume
from recruit_ai.candidate.schema import CandidateProfile


RESUME_FOLDER = Path("data/raw/resumes")


def load_candidates() -> list[CandidateProfile]:
    """
    Load and parse every resume in the resume folder.
    """

    candidates = []

    if not RESUME_FOLDER.exists():
        return candidates

    for pdf in sorted(RESUME_FOLDER.glob("*.pdf")):

        try:
            text = extract_text(str(pdf))

            candidate = parse_resume(text)

            candidates.append(candidate)

        except Exception as e:

            print(f"Failed to load {pdf.name}")

            print(e)

    return candidates