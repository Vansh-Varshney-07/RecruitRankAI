SECTION_HEADERS = [
    "REQUIRED SKILLS",
    "PREFERRED SKILLS",
    "RESPONSIBILITIES",
    "EDUCATION",
    "EXPERIENCE",
]


def extract_section(text: str, section_name: str):
    """
    Extract lines from a job section until another section starts.
    """

    lines = text.splitlines()

    collecting = False

    collected = []

    for line in lines:

        stripped = line.strip()

        if stripped.upper() == section_name.upper():
            collecting = True
            continue

        if collecting:

            if stripped.upper() in SECTION_HEADERS:
                break

            if stripped:
                collected.append(stripped)

    return collected