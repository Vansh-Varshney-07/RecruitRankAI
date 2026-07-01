import json
from dataclasses import dataclass

from ollama import Client

from recruit_ai.candidate.schema import CandidateProfile
from recruit_ai.job.schema import JobProfile
from recruit_ai.reasoning.explanation import match_explanation


DEFAULT_MODEL = "qwen2.5-coder:7b-instruct"
DEFAULT_HOST = "http://127.0.0.1:11434"


@dataclass
class RecruiterBrainResult:
    summary: str
    strengths: list[str]
    risks: list[str]
    interview_questions: list[str]
    score_delta: float = 0.0
    used_llm: bool = False


def _candidate_brief(candidate: CandidateProfile) -> dict:
    return {
        "candidate_id": candidate.candidate_id,
        "name": candidate.name,
        "headline": candidate.headline,
        "location": candidate.location,
        "years_of_experience": candidate.years_of_experience,
        "skills": [
            {
                "name": skill.name,
                "proficiency": skill.proficiency,
                "endorsements": skill.endorsements,
                "duration_months": skill.duration_months,
            }
            for skill in candidate.skills[:25]
        ],
        "recent_roles": [
            {
                "title": item.title,
                "company": item.company,
                "duration_months": item.duration_months,
                "description": item.description[:500],
            }
            for item in candidate.experience[:3]
        ],
        "signals": candidate.signals,
        "summary": candidate.raw_text[:1200],
    }


def _job_brief(job: JobProfile) -> dict:
    return {
        "title": job.title,
        "required_skills": job.required_skills,
        "preferred_skills": job.preferred_skills,
        "experience": job.experience,
        "education": job.education,
        "responsibilities": job.responsibilities,
        "description": job.description[:1800],
    }


def _fallback_review(
    candidate: CandidateProfile,
    job: JobProfile,
    breakdown: dict,
) -> RecruiterBrainResult:
    explanation = match_explanation(
        candidate,
        job,
        breakdown,
    )
    missing = explanation["missing_skills"]
    risks = []

    if missing:
        risks.append(f"Missing direct evidence for: {', '.join(missing[:4])}.")

    if candidate.signals.get("notice_period_days", 0) and candidate.signals["notice_period_days"] > 90:
        risks.append("Long notice period may slow hiring velocity.")

    if not risks:
        risks.append("No major deterministic risk surfaced; validate depth in interview.")

    return RecruiterBrainResult(
        summary=" ".join(explanation["reasons"]),
        strengths=explanation["matched_skills"][:5] or ["Relevant profile signals present."],
        risks=risks,
        interview_questions=[
            "Walk through the most relevant project or role for this job.",
            "Which required skill have you used most recently in production?",
            "What would you need to learn in the first 30 days?",
        ],
        used_llm=False,
    )


def _coerce_result(payload: dict) -> RecruiterBrainResult:
    return RecruiterBrainResult(
        summary=str(payload.get("summary", "")).strip()[:500],
        strengths=[str(item)[:180] for item in payload.get("strengths", [])[:5]],
        risks=[str(item)[:180] for item in payload.get("risks", [])[:5]],
        interview_questions=[
            str(item)[:180]
            for item in payload.get("interview_questions", [])[:5]
        ],
        score_delta=max(
            -0.08,
            min(
                float(payload.get("score_delta", 0.0) or 0.0),
                0.08,
            ),
        ),
        used_llm=True,
    )


def review_candidate_with_llm(
    candidate: CandidateProfile,
    job: JobProfile,
    breakdown: dict,
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_HOST,
    timeout: int = 20,
) -> RecruiterBrainResult:
    """
    Ask a local LLM for shortlist-level recruiter judgment.

    Falls back to deterministic explanations when Ollama is unavailable or the
    model returns invalid JSON.
    """

    fallback = _fallback_review(candidate, job, breakdown)
    client = Client(host=host, timeout=timeout)

    prompt = {
        "job": _job_brief(job),
        "candidate": _candidate_brief(candidate),
        "deterministic_breakdown": breakdown,
        "instructions": [
            "Act as a senior AI recruiter.",
            "Judge contextual fit, hidden signals, risks, and recruiter actionability.",
            "Do not invent facts not present in the input.",
            "Return JSON only with keys: summary, strengths, risks, interview_questions, score_delta.",
            "score_delta must be between -0.08 and 0.08.",
        ],
    }

    try:
        response = client.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are RecruitRankAI's shortlist judge. Return strict JSON only.",
                },
                {
                    "role": "user",
                    "content": json.dumps(prompt),
                },
            ],
            format="json",
        )
        payload = json.loads(response["message"]["content"])
        result = _coerce_result(payload)

        if not result.summary:
            return fallback

        return result

    except Exception:
        return fallback


def apply_llm_score_delta(item: dict, review: RecruiterBrainResult) -> dict:
    adjusted = dict(item)
    adjusted_breakdown = dict(item["breakdown"])
    adjusted_score = max(
        0.0,
        min(
            1.0,
            item["score"] + review.score_delta,
        ),
    )

    adjusted["score"] = round(adjusted_score, 3)
    adjusted_breakdown["overall"] = adjusted["score"]
    adjusted["breakdown"] = adjusted_breakdown
    adjusted["llm_review"] = review
    return adjusted
