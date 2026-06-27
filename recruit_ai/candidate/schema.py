from dataclasses import dataclass, field


@dataclass
class CandidateProfile:
    name: str = ""

    email: str = ""
    phone: str = ""

    education: list[str] = field(default_factory=list)

    experience: list[str] = field(default_factory=list)

    skills: list[str] = field(default_factory=list)

    projects: list[str] = field(default_factory=list)

    certifications: list[str] = field(default_factory=list)

    research_interests: list[str] = field(default_factory=list)

    raw_text: str = ""

@dataclass
class Project:

    title: str

    description: str

from dataclasses import dataclass, field


# -----------------------------
# Skill
# -----------------------------

@dataclass
class Skill:
    name: str
    category: str = ""
    confidence: float = 1.0


# -----------------------------
# Education
# -----------------------------

@dataclass
class Education:
    degree: str
    institute: str = ""
    year: str = ""


# -----------------------------
# Project
# -----------------------------

@dataclass
class Project:
    title: str
    summary: str = ""
    technologies: list[str] = field(default_factory=list)


# -----------------------------
# Certification
# -----------------------------

@dataclass
class Certification:
    name: str
    provider: str = ""


# -----------------------------
# Research Interest
# -----------------------------

@dataclass
class ResearchInterest:
    topic: str


# -----------------------------
# Experience
# -----------------------------

@dataclass
class Experience:
    title: str


# -----------------------------
# Candidate
# -----------------------------

@dataclass
class CandidateProfile:

    name: str = ""

    email: str = ""

    phone: str = ""

    skills: list[Skill] = field(default_factory=list)

    education: list[Education] = field(default_factory=list)

    experience: list[Experience] = field(default_factory=list)

    projects: list[Project] = field(default_factory=list)

    certifications: list[Certification] = field(default_factory=list)

    research_interests: list[ResearchInterest] = field(default_factory=list)

    raw_text: str = ""