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
        skill.lower()
        for skill in candidate.skills
    }

    required_skills = {
        skill.lower()
        for skill in job.required_skills
    }

    if not required_skills:
        return 0.0

    matched = candidate_skills & required_skills

    return len(matched) / len(required_skills)