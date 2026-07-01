import re


SECTION_ALIASES = {
    "REQUIRED SKILLS": {
        "required skills",
        "must have skills",
        "requirements",
        "required qualifications",
        "qualifications",
    },
    "PREFERRED SKILLS": {
        "preferred skills",
        "nice to have",
        "good to have",
        "preferred qualifications",
    },
    "RESPONSIBILITIES": {
        "responsibilities",
        "what you will do",
        "role responsibilities",
        "key responsibilities",
    },
    "EDUCATION": {
        "education",
        "education requirements",
        "academic requirements",
    },
    "EXPERIENCE": {
        "experience",
        "experience requirements",
        "work experience",
    },
}


def _normalize_heading(line: str) -> str:
    normalized = re.sub(r"^[#*\-\u2022\s]+", "", line)
    normalized = normalized.strip().rstrip(":").strip()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.lower()


def _canonical_heading(line: str) -> str | None:
    normalized = _normalize_heading(line)

    for canonical, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return canonical

    return None


def extract_section(text: str, section_name: str) -> list[str]:
    """
    Extract lines from a job section until another known section starts.
    """

    target = section_name.upper()
    collecting = False
    collected = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        heading = _canonical_heading(stripped)

        if heading == target:
            collecting = True
            continue

        if heading and collecting:
            break

        if collecting:
            collected.append(stripped)

    return collected
