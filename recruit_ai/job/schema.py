from dataclasses import dataclass, field


@dataclass
class JobProfile:

    title: str = ""

    company: str = ""

    description: str = ""

    required_skills: list[str] = field(default_factory=list)

    preferred_skills: list[str] = field(default_factory=list)

    education: list[str] = field(default_factory=list)

    experience: list[str] = field(default_factory=list)

    responsibilities: list[str] = field(default_factory=list)

    keywords: list[str] = field(default_factory=list)