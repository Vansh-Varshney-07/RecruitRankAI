from pathlib import Path

from recruit_ai.job.parser import parse_job
from recruit_ai.ranking.batch_ranker import rank_candidates
from recruit_ai.ranking.export_csv import export_results
from recruit_ai.reasoning.recommendation import recommend


JOB = Path("data/raw/jobs/job1.txt")
DATASET = Path("data/redrob/candidates.jsonl")


job = parse_job(
    JOB.read_text(encoding="utf-8")
)

results = rank_candidates(
    DATASET,
    job,
)

export_results(
    results,
    "ranking.csv",
)

for i,item in enumerate(results[:10],1):

    s=item["breakdown"]

    print(
        f"""{i:2d}.
{item['candidate'].name}

Overall      : {s['overall']}
Skill        : {s['skill']}
Semantic     : {s['semantic']}
Experience   : {s['experience']}
Education    : {s['education']}
Projects     : {s['projects']}
"""
    )

print("="*80)
print("TOP 10")
print("="*80)
print(
    "Recommendation:",
    recommend(s["overall"])
)
