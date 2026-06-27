import re

from recruit_ai.job.schema import JobProfile
from recruit_ai.job.section_parser import extract_section
from recruit_ai.job.skill_parser import extract_skills


def parse_job(text: str) -> JobProfile:

    profile = JobProfile()

    profile.description = text

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:
        profile.title = lines[0]

    # Required Skills
    required = extract_section(
        text,
        "REQUIRED SKILLS",
    )

    profile.required_skills = extract_skills(required)

    # Preferred Skills
    preferred = extract_section(
        text,
        "PREFERRED SKILLS",
    )

    profile.preferred_skills = extract_skills(preferred)

    # Responsibilities
    profile.responsibilities = extract_section(
        text,
        "RESPONSIBILITIES",
    )

    # Education
    profile.education = extract_section(
        text,
        "EDUCATION",
    )

    # Experience
    profile.experience = extract_section(
        text,
        "EXPERIENCE",
    )

    return profile