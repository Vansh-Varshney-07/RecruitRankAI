from pathlib import Path
from typing import Iterable

from recruit_ai.job.schema import JobProfile
from recruit_ai.ranking.scorer import overall_score
from recruit_ai.redrob.feature_engine import build_candidate
from recruit_ai.redrob.loader import load_candidates


DEFAULT_DATASET = Path("data/redrob/candidates.jsonl")


def rank_redrob_candidates(
    job: JobProfile,
    dataset_path: str | Path = DEFAULT_DATASET,
    limit: int | None = 1000,
) -> list[dict]:
    """
    Rank Redrob candidates against a parsed job profile.

    The optional limit keeps interactive UI runs responsive while still using
    real candidate data. Batch jobs can pass None to score the full dataset.
    """

    rankings = []

    for index, candidate_json in enumerate(load_candidates(dataset_path)):
        if limit is not None and index >= limit:
            break

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
        key=lambda item: (
            -item["score"],
            -item["breakdown"]["skill"],
            -item["breakdown"]["semantic"],
            item["candidate"].candidate_id,
        ),
    )

    return rankings


def filter_rankings(
    rankings: Iterable[dict],
    minimum_score: float = 0.0,
) -> list[dict]:
    return [
        item
        for item in rankings
        if item["score"] >= minimum_score
    ]
