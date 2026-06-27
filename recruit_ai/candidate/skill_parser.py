import re

from recruit_ai.candidate.schema import Skill


SKILL_SECTIONS = [
    "technical skills",
    "skills",
]


def extract_skills(sections: dict) -> list[Skill]:

    skills = []

    for section_name in SKILL_SECTIONS:

        if section_name not in sections:
            continue

        text = sections[section_name]

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            # Ignore section headings
            if line.upper() == line:
                continue

            line = line.replace("•", ",")

            parts = [
                x.strip()
                for x in re.split(r",|:", line)
            ]

            for part in parts:

                if len(part) < 2:
                    continue

                skills.append(
                    Skill(
                        name=part
                    )
                )

    # Remove duplicates while preserving order
    unique_skills = []
    seen = set()

    for skill in skills:

        if skill.name.lower() in seen:
            continue

        seen.add(skill.name.lower())
        unique_skills.append(skill)

    return unique_skills