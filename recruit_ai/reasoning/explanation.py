from recruit_ai.candidate.schema import CandidateProfile
from recruit_ai.job.schema import JobProfile


def _candidate_skill_names(candidate: CandidateProfile) -> set[str]:
    return {
        skill.name.lower()
        for skill in candidate.skills
        if skill.name
    }


def match_explanation(
    candidate: CandidateProfile,
    job: JobProfile,
    breakdown: dict,
) -> dict:
    candidate_skills = _candidate_skill_names(candidate)

    matched = [
        skill
        for skill in job.required_skills
        if skill.lower() in candidate_skills
    ]

    missing = [
        skill
        for skill in job.required_skills
        if skill.lower() not in candidate_skills
    ]

    reasons = []

    if matched:
        reasons.append(f"Matches {len(matched)} required skill signals.")

    if candidate.years_of_experience:
        reasons.append(f"{candidate.years_of_experience:.1f} years of experience.")

    if breakdown.get("semantic", 0) >= 0.75:
        reasons.append("Strong semantic overlap with the job profile.")

    if candidate.signals.get("open_to_work_flag"):
        reasons.append("Open-to-work signal is active.")

    if not reasons:
        reasons.append("Limited direct signal match; review manually.")

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "reasons": reasons,
    }
