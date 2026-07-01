from difflib import SequenceMatcher


def semantic_similarity(a: str, b: str) -> float:
    """
    Lightweight text similarity used as the local default.

    This keeps ranking deterministic and offline. A true embedding-based
    matcher can be added later without changing scorer contracts.
    """

    return SequenceMatcher(
        None,
        str(a).lower(),
        str(b).lower()
    ).ratio()


def similarity(a: str, b: str) -> float:
    return semantic_similarity(a, b)


def semantic_skill_score(candidate, job):

    if not job.required_skills:
        return 0.0

    matched = 0.0

    candidate_skills = [
        s.name.lower()
        for s in candidate.skills
        if s.name
    ]

    for req in job.required_skills:

        req = req.lower()

        best = 0.0

        for skill in candidate_skills:

            score = semantic_similarity(req, skill)

            if score > best:

                best = score

        matched += best

    return matched / len(job.required_skills)
