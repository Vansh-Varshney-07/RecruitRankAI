from recruit_ai.candidate.schema import CandidateProfile, Skill
from recruit_ai.job.schema import JobProfile
from recruit_ai.reasoning.explanation import match_explanation


def test_match_explanation_reports_matched_and_missing_skills():
    candidate = CandidateProfile(
        name="Asha",
        years_of_experience=4,
        skills=[
            Skill("Python"),
            Skill("SQL"),
        ],
    )
    job = JobProfile(
        required_skills=[
            "Python",
            "PyTorch",
        ]
    )

    explanation = match_explanation(
        candidate,
        job,
        {"semantic": 0.8},
    )

    assert explanation["matched_skills"] == ["Python"]
    assert explanation["missing_skills"] == ["PyTorch"]
    assert "Strong semantic overlap" in " ".join(explanation["reasons"])
