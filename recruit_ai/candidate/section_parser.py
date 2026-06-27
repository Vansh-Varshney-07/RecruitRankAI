SECTION_HEADERS = [
    "education",
    "technical skills",
    "skills",
    "projects",
    "projects & independent research",
    "experience",
    "certifications",
    "research interests",
]


def split_into_sections(text: str) -> dict:
    """
    Split a resume into named sections.

    Returns:
    {
        "education": "...",
        "technical skills": "...",
        ...
    }
    """

    sections = {}

    current_section = None
    buffer = []

    for line in text.splitlines():

        stripped = line.strip()

        if not stripped:
            continue

        lower = stripped.lower()

        if lower in SECTION_HEADERS:

            if current_section is not None:

                sections[current_section] = "\n".join(buffer)

            current_section = lower
            buffer = []

            continue

        if current_section is not None:
            buffer.append(stripped)

    if current_section is not None:
        sections[current_section] = "\n".join(buffer)

    return sections