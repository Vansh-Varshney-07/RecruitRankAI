import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from recruit_ai.job.parser import parse_job
from recruit_ai.ranking.redrob_ranker import filter_rankings, rank_redrob_candidates
from recruit_ai.reasoning.explanation import match_explanation
from recruit_ai.reasoning.recommendation import recommend
from recruit_ai.reasoning.recruiter_brain import apply_llm_score_delta
from recruit_ai.reasoning.recruiter_brain import review_candidate_with_llm


DATASET_PATH = Path(
    os.getenv(
        "RECRUITRANKAI_DATASET",
        "data/redrob/candidates.jsonl",
    )
)
SAMPLE_DATASET_PATH = Path("data/redrob/sample_candidates.json")

DEFAULT_JOB_PATH = Path(
    os.getenv(
        "RECRUITRANKAI_DEFAULT_JOB",
        "data/raw/jobs/job1.txt",
    )
)


def _cors_origins() -> list[str]:
    raw = os.getenv("RECRUITRANKAI_API_CORS_ORIGINS", "*")

    if raw.strip() == "*":
        return ["*"]

    return [
        item.strip()
        for item in raw.split(",")
        if item.strip()
    ]


app = FastAPI(
    title="RecruitRankAI API",
    version="1.0.0",
    description="Signal-first candidate ranking API with optional local LLM review.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RankRequest(BaseModel):
    job_text: str | None = Field(
        default=None,
        description="Raw job description text. Uses default job file when omitted.",
    )
    scan_limit: int = Field(default=1000, ge=1, le=100000)
    minimum_score: float = Field(default=0.0, ge=0.0, le=1.0)
    top_n: int = Field(default=25, ge=1, le=100)
    use_llm: bool = False
    llm_limit: int = Field(default=5, ge=1, le=25)


def _default_job_text() -> str:
    if DEFAULT_JOB_PATH.exists():
        return DEFAULT_JOB_PATH.read_text(encoding="utf-8")

    return "Machine Learning Engineer\n\nREQUIRED SKILLS\n\nPython\nSQL\nMachine Learning"


def _active_dataset_path() -> Path:
    if DATASET_PATH.exists():
        return DATASET_PATH

    if SAMPLE_DATASET_PATH.exists():
        return SAMPLE_DATASET_PATH

    return DATASET_PATH


def _candidate_payload(item: dict, job) -> dict:
    candidate = item["candidate"]
    explanation = match_explanation(
        candidate,
        job,
        item["breakdown"],
    )
    review = item.get("llm_review")

    return {
        "candidate_id": candidate.candidate_id,
        "name": candidate.name,
        "headline": candidate.headline,
        "location": candidate.location,
        "years_of_experience": candidate.years_of_experience,
        "score": item["score"],
        "recommendation": recommend(item["score"]),
        "breakdown": item["breakdown"],
        "matched_skills": explanation["matched_skills"],
        "missing_skills": explanation["missing_skills"],
        "reasons": explanation["reasons"],
        "llm_review": None
        if review is None
        else {
            "summary": review.summary,
            "strengths": review.strengths,
            "risks": review.risks,
            "interview_questions": review.interview_questions,
            "score_delta": review.score_delta,
            "used_llm": review.used_llm,
        },
    }


@app.get("/health")
def health() -> dict:
    active_dataset = _active_dataset_path()

    return {
        "status": "ok",
        "dataset_exists": DATASET_PATH.exists(),
        "dataset_path": str(DATASET_PATH),
        "active_dataset_path": str(active_dataset),
        "using_sample_dataset": active_dataset == SAMPLE_DATASET_PATH,
        "default_job_exists": DEFAULT_JOB_PATH.exists(),
    }


@app.post("/rank")
def rank_candidates_api(request: RankRequest) -> dict:
    dataset_path = _active_dataset_path()

    if not dataset_path.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Candidate dataset not found at {DATASET_PATH} or {SAMPLE_DATASET_PATH}.",
        )

    job_text = request.job_text or _default_job_text()
    job = parse_job(job_text)
    rankings = rank_redrob_candidates(
        job,
        dataset_path=dataset_path,
        limit=request.scan_limit,
    )
    filtered = filter_rankings(
        rankings,
        request.minimum_score,
    )

    if request.use_llm:
        reviewed = []

        for index, item in enumerate(filtered):
            if index >= request.llm_limit:
                reviewed.append(item)
                continue

            review = review_candidate_with_llm(
                item["candidate"],
                job,
                item["breakdown"],
            )
            reviewed.append(
                apply_llm_score_delta(
                    item,
                    review,
                )
            )

        filtered = sorted(
            reviewed,
            key=lambda item: (
                -item["score"],
                item["candidate"].candidate_id,
            ),
        )

    selected = filtered[: request.top_n]

    return {
        "job": {
            "title": job.title,
            "required_skills": job.required_skills,
            "preferred_skills": job.preferred_skills,
        },
        "using_sample_dataset": dataset_path == SAMPLE_DATASET_PATH,
        "count": len(selected),
        "results": [
            _candidate_payload(item, job)
            for item in selected
        ],
    }
