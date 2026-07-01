from recruit_ai.candidate.schema import CandidateProfile, Education, Experience, Skill
from recruit_ai.job.schema import JobProfile
from recruit_ai.ranking.hybrid_matcher import hybrid_skill_score
from recruit_ai.ranking.redrob_ranker import filter_rankings
from recruit_ai.ranking.scorer import experience_score, overall_score
from recruit_ai.ranking.semantic_matcher import semantic_similarity
from recruit_ai.redrob.feature_engine import build_candidate


def test_semantic_similarity_is_importable_and_deterministic():
    assert semantic_similarity("Python", "Python") == 1.0
    assert semantic_similarity("Python", "Cooking") < 1.0


def test_hybrid_skill_score_uses_skill_names():
    candidate = CandidateProfile(
        skills=[
            Skill("Python"),
            Skill("Machine Learning"),
        ]
    )
    job = JobProfile(
        required_skills=[
            "Python",
            "Machine Learning",
        ]
    )

    assert hybrid_skill_score(candidate, job) == 1.0


def test_experience_score_uses_profile_years_before_parsed_entries():
    candidate = CandidateProfile(
        years_of_experience=6,
        experience=[
            Experience(
                title="Engineer",
                duration_months=12,
            )
        ],
    )

    assert experience_score(candidate) == 1.0


def test_overall_score_has_expected_breakdown_keys():
    candidate = CandidateProfile(
        years_of_experience=3,
        skills=[Skill("Python")],
        education=[
            Education(
                degree="B.Tech",
                field_of_study="Computer Science",
            )
        ],
    )
    job = JobProfile(required_skills=["Python"])

    score = overall_score(candidate, job)

    assert set(score) == {
        "skill",
        "semantic",
        "experience",
        "education",
        "projects",
        "overall",
    }
    assert score["overall"] > 0


def test_redrob_candidate_builder_maps_current_schema():
    raw = {
        "candidate_id": "CAND_0000001",
        "profile": {
            "anonymized_name": "Asha Rao",
            "headline": "ML Engineer",
            "location": "Bengaluru",
            "years_of_experience": 4.5,
            "summary": "Builds ranking systems.",
        },
        "skills": [
            {
                "name": "Python",
                "proficiency": "advanced",
                "endorsements": 12,
                "duration_months": 36,
            }
        ],
        "education": [
            {
                "institution": "Example Institute",
                "degree": "B.Tech",
                "field_of_study": "Computer Science",
                "end_year": 2020,
            }
        ],
        "career_history": [
            {
                "company": "Example Co",
                "title": "ML Engineer",
                "duration_months": 30,
                "description": "Built ML systems.",
                "is_current": True,
            }
        ],
        "certifications": [
            {
                "name": "ML Cert",
                "issuer": "Example Org",
            }
        ],
        "redrob_signals": {
            "profile_completeness_score": 90,
        },
    }

    candidate = build_candidate(raw)

    assert candidate.candidate_id == "CAND_0000001"
    assert candidate.name == "Asha Rao"
    assert candidate.skills[0].duration_months == 36
    assert candidate.education[0].institute == "Example Institute"
    assert candidate.experience[0].duration_months == 30
    assert candidate.certifications[0].provider == "Example Org"
    assert candidate.signals["profile_completeness_score"] == 90


def test_filter_rankings_applies_minimum_score():
    rankings = [
        {"score": 0.9},
        {"score": 0.5},
    ]

    assert filter_rankings(rankings, 0.75) == [{"score": 0.9}]
