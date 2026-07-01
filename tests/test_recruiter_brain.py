from recruit_ai.candidate.schema import CandidateProfile, Skill
from recruit_ai.job.schema import JobProfile
from recruit_ai.reasoning.recruiter_brain import apply_llm_score_delta
from recruit_ai.reasoning.recruiter_brain import review_candidate_with_llm


def test_recruiter_brain_falls_back_when_ollama_is_unavailable():
    candidate = CandidateProfile(
        name="Asha",
        years_of_experience=5,
        skills=[Skill("Python")],
    )
    job = JobProfile(required_skills=["Python", "PyTorch"])

    review = review_candidate_with_llm(
        candidate,
        job,
        {"semantic": 0.8},
        host="http://127.0.0.1:1",
        timeout=1,
    )

    assert review.used_llm is False
    assert review.summary
    assert review.interview_questions


def test_apply_llm_score_delta_clamps_score():
    candidate = CandidateProfile(candidate_id="CAND_1")
    item = {
        "candidate": candidate,
        "score": 0.99,
        "breakdown": {"overall": 0.99},
    }
    review = review_candidate_with_llm(
        candidate,
        JobProfile(),
        {},
        host="http://127.0.0.1:1",
        timeout=1,
    )
    review.score_delta = 0.5

    adjusted = apply_llm_score_delta(item, review)

    assert adjusted["score"] == 1.0
    assert adjusted["breakdown"]["overall"] == 1.0
