from recruit_ai.candidate.schema import CandidateProfile
from recruit_ai.job.schema import JobProfile


def skill_match_score(
    candidate: CandidateProfile,
    job: JobProfile,
) -> float:
    """
    Calculate percentage of required skills matched.
    """

    candidate_skills = {
        s.name.lower()
        for s in candidate.skills
        if s.name
    }

    required_skills = {
        s.lower()
        for s in job.required_skills
        if s
    }

    if not required_skills:
        return 0.0

    matched = candidate_skills & required_skills

    return len(matched) / len(required_skills)
