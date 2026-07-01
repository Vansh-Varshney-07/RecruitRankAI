import re


SPLIT_PATTERN = re.compile(r",|;|\u2022|\n")


def _clean_item(value: str) -> str:
    value = re.sub(r"^[\-*\u2022\d.)\s]+", "", value)
    value = value.strip(" \t:-")
    return re.sub(r"\s+", " ", value)


def extract_skills(lines: list[str]) -> list[str]:
    """
    Extract individual skills from job description section lines.
    """

    skills = []
    seen = set()

    for line in lines:
        for part in SPLIT_PATTERN.split(line):
            skill = _clean_item(part)

            if not skill:
                continue

            key = skill.lower()

            if key in seen:
                continue

            seen.add(key)
            skills.append(skill)

    return skills
