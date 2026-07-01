from recruit_ai.ranking.matcher import skill_match_score
from recruit_ai.ranking.semantic_matcher import semantic_skill_score


def _total_experience_years(candidate) -> float:
    if candidate.years_of_experience:
        return float(candidate.years_of_experience)

    months = sum(
        getattr(item, "duration_months", 0) or 0
        for item in candidate.experience
    )

    if months:
        return months / 12

    for item in candidate.experience:
        duration = str(getattr(item, "duration", "")).strip()

        if not duration:
            continue

        try:
            return float(duration.split()[0])
        except (TypeError, ValueError):
            continue

    return 0.0


def experience_score(candidate):

    years = _total_experience_years(candidate)

    if not years:
        return 0.0

    return min(years / 5, 1.0)


def education_score(candidate):

    if not candidate.education:
        return 0

    degree = candidate.education[0].degree.lower()
    field = getattr(candidate.education[0], "field_of_study", "").lower()
    education_text = f"{degree} {field}"

    if "phd" in education_text or "ph.d" in education_text:
        return 1

    if "master" in education_text or "m.tech" in education_text or "m.s" in education_text:
        return 0.9

    if "b.tech" in education_text or "b.e" in education_text or "b.sc" in education_text:
        return 0.8

    return 0.5


def project_score(candidate):

    n = len(candidate.projects)

    return min(n / 5, 1.0)


def overall_score(candidate, job):

    skill = skill_match_score(candidate, job)

    semantic = semantic_skill_score(candidate, job)

    experience = experience_score(candidate)

    education = education_score(candidate)

    projects = project_score(candidate)

    overall = (
        0.35 * skill +
        0.25 * semantic +
        0.20 * experience +
        0.10 * education +
        0.10 * projects
    )

    return {
        "skill": round(skill, 3),
        "semantic": round(semantic, 3),
        "experience": round(experience, 3),
        "education": round(education, 3),
        "projects": round(projects, 3),
        "overall": round(overall, 3),
    }
