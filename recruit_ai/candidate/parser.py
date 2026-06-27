import re

from recruit_ai.candidate.schema import CandidateProfile

from recruit_ai.candidate.section_parser import split_into_sections

from recruit_ai.candidate.skill_parser import extract_skills
from recruit_ai.candidate.education_parser import extract_education
from recruit_ai.candidate.project_parser import extract_projects
from recruit_ai.candidate.certification_parser import extract_certifications
from recruit_ai.candidate.research_parser import extract_research
from recruit_ai.candidate.experience_parser import extract_experience


# -------------------------------------------------
# Regular Expressions
# -------------------------------------------------

EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_PATTERN = r"(\+?\d[\d\s-]{8,}\d)"


# -------------------------------------------------
# Resume Parser
# -------------------------------------------------

def parse_resume(text: str) -> CandidateProfile:
    """
    Convert raw resume text into a structured CandidateProfile.
    """

    profile = CandidateProfile()

    profile.raw_text = text

    # -------------------------------------------------
    # Name
    # -------------------------------------------------

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:
        profile.name = lines[0]

    # -------------------------------------------------
    # Email
    # -------------------------------------------------

    email = re.search(EMAIL_PATTERN, text)

    if email:
        profile.email = email.group()

    # -------------------------------------------------
    # Phone
    # -------------------------------------------------

    phone = re.search(PHONE_PATTERN, text)

    if phone:
        profile.phone = phone.group()

    # -------------------------------------------------
    # Split Resume into Sections
    # -------------------------------------------------

    sections = split_into_sections(text)

    # -------------------------------------------------
    # Structured Parsing
    # -------------------------------------------------

    profile.skills = extract_skills(sections)

    profile.education = extract_education(sections)

    profile.projects = extract_projects(sections)

    profile.certifications = extract_certifications(sections)

    profile.research_interests = extract_research(sections)

    profile.experience = extract_experience(sections)

    return profile