import argparse
import csv
from pathlib import Path

from recruit_ai.job.parser import parse_job
from recruit_ai.ranking.redrob_ranker import rank_redrob_candidates
from recruit_ai.reasoning.explanation import match_explanation


DEFAULT_DATASET = Path("data/redrob/candidates.jsonl")
DEFAULT_JOB = Path("data/raw/jobs/job1.txt")
DEFAULT_OUTPUT = Path("data/output/recruitrankai_submission.csv")


def _reasoning(item: dict, job) -> str:
    candidate = item["candidate"]
    explanation = match_explanation(
        candidate,
        job,
        item["breakdown"],
    )
    matched = ", ".join(explanation["matched_skills"][:4]) or "semantic/profile fit"
    missing = ", ".join(explanation["missing_skills"][:3])
    risk = f" Missing: {missing}." if missing else ""

    return (
        f"{candidate.headline or 'Candidate'} with "
        f"{candidate.years_of_experience:.1f} yrs; matched {matched}; "
        f"score {item['score']:.3f}.{risk}"
    )[:500]


def generate_submission(
    job_path: str | Path = DEFAULT_JOB,
    dataset_path: str | Path = DEFAULT_DATASET,
    output_path: str | Path = DEFAULT_OUTPUT,
    top_n: int = 100,
    scan_limit: int | None = None,
) -> Path:
    job_text = Path(job_path).read_text(encoding="utf-8")
    job = parse_job(job_text)
    rankings = rank_redrob_candidates(
        job,
        dataset_path=dataset_path,
        limit=scan_limit,
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])

        for rank, item in enumerate(rankings[:top_n], start=1):
            writer.writerow(
                [
                    item["candidate"].candidate_id,
                    rank,
                    f"{item['score']:.4f}",
                    _reasoning(item, job),
                ]
            )

    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate RecruitRankAI hackathon submission CSV."
    )
    parser.add_argument("--job", default=str(DEFAULT_JOB))
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--top-n", type=int, default=100)
    parser.add_argument(
        "--scan-limit",
        type=int,
        default=None,
        help="Limit candidates for quick local runs. Omit for full dataset.",
    )
    args = parser.parse_args()

    output = generate_submission(
        job_path=args.job,
        dataset_path=args.dataset,
        output_path=args.output,
        top_n=args.top_n,
        scan_limit=args.scan_limit,
    )
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
