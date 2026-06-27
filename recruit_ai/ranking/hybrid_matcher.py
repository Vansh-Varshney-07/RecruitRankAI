from recruit_ai.candidate.schema import CandidateProfile
from recruit_ai.job.schema import JobProfile

from recruit_ai.ranking.semantic_matcher import semantic_similarity


SIMILARITY_THRESHOLD = 0.75


def hybrid_skill_score(
    candidate: CandidateProfile,
    job: JobProfile,
) -> float:

    matched = 0

    for required_skill in job.required_skills:

        for candidate_skill in candidate.skills:

            score = semantic_similarity(
                required_skill,
                candidate_skill,
            )

            if score >= SIMILARITY_THRESHOLD:

                matched += 1

                break

    if not job.required_skills:
        return 0.0

    return matched / len(job.required_skills)