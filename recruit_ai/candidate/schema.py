from dataclasses import dataclass, field


@dataclass
class Skill:
    name: str
    category: str = ""
    confidence: float = 1.0
    proficiency: str = ""
    endorsements: int = 0
    duration_months: int = 0


@dataclass
class Education:
    degree: str
    institute: str = ""
    year: str = ""
    field_of_study: str = ""


@dataclass
class Experience:
    title: str
    company: str = ""
    duration: str = ""
    duration_months: int = 0
    description: str = ""
    is_current: bool = False


@dataclass
class Project:
    title: str
    summary: str = ""
    technologies: list[str] = field(default_factory=list)


@dataclass
class Certification:
    name: str
    provider: str = ""


@dataclass
class ResearchInterest:
    topic: str


@dataclass
class CandidateProfile:
    name: str = ""
    email: str = ""
    phone: str = ""
    candidate_id: str = ""
    headline: str = ""
    location: str = ""
    years_of_experience: float = 0.0
    skills: list[Skill] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)
    research_interests: list[ResearchInterest] = field(default_factory=list)
    signals: dict = field(default_factory=dict)
    raw_text: str = ""
