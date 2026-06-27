from recruit_ai.ranking.matcher import skill_match_score


def overall_score(
    candidate,
    job,
):
    """
    Combine multiple scores into one final score.
    """

    scores = {}

    # -------------------------
    # Skill Score
    # -------------------------

    scores["skill"] = skill_match_score(
        candidate,
        job,
    )

    # -------------------------
    # Future Scores
    # -------------------------

    scores["education"] = 0.0

    scores["experience"] = 0.0

    scores["projects"] = 0.0

    scores["research"] = 0.0

    # -------------------------
    # Weighted Sum
    # -------------------------

    final = (
        scores["skill"] * 1.0
    )

    scores["overall"] = final

    return scores