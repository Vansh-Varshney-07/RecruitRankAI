from recruit_ai.ranking.scorer import overall_score
from recruit_ai.candidate.schema import CandidateProfile
from recruit_ai.job.schema import JobProfile


def rank_candidates(
    candidates: list[CandidateProfile],
    job: JobProfile,
):
    """
    Score every candidate against a job
    and return them sorted from best to worst.
    """

    ranked = []

    for candidate in candidates:

        score = overall_score(
            candidate,
            job,
        )

        ranked.append(
            {
                "candidate": candidate,
                "score": score,
            }
        )

    ranked.sort(
        key=lambda x: x["score"]["overall"],
        reverse=True,
    )

    return ranked