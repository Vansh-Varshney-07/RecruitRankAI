from recruit_ai.redrob.loader import load_candidates
from recruit_ai.redrob.feature_engine import build_candidate
from recruit_ai.ranking.scorer import overall_score


def rank_candidates(dataset_path, job):

    rankings = []

    for candidate_json in load_candidates(dataset_path):

        candidate = build_candidate(candidate_json)

        scores = overall_score(candidate, job)

        rankings.append(
            {
                "candidate": candidate,
                "score": scores["overall"],
                "breakdown": scores,
            }
        )

    rankings.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return rankings