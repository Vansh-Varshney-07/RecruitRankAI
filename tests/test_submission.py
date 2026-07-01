from pathlib import Path

from recruit_ai.submission.generate_submission import generate_submission


def test_generate_submission_writes_required_columns(tmp_path):
    job_path = tmp_path / "job.txt"
    dataset_path = tmp_path / "candidates.jsonl"
    output_path = tmp_path / "submission.csv"

    job_path.write_text(
        "ML Engineer\n\nREQUIRED SKILLS\n\nPython\nSQL",
        encoding="utf-8",
    )
    dataset_path.write_text(
        """
{"candidate_id":"CAND_0000001","profile":{"anonymized_name":"Asha","headline":"ML Engineer","years_of_experience":5},"career_history":[],"education":[],"skills":[{"name":"Python"},{"name":"SQL"}],"certifications":[],"redrob_signals":{}}
{"candidate_id":"CAND_0000002","profile":{"anonymized_name":"Ravi","headline":"Designer","years_of_experience":2},"career_history":[],"education":[],"skills":[{"name":"Figma"}],"certifications":[],"redrob_signals":{}}
""".strip(),
        encoding="utf-8",
    )

    output = generate_submission(
        job_path=job_path,
        dataset_path=dataset_path,
        output_path=output_path,
        top_n=2,
    )

    lines = Path(output).read_text(encoding="utf-8").splitlines()

    assert lines[0] == "candidate_id,rank,score,reasoning"
    assert lines[1].startswith("CAND_0000001,1,")
    assert len(lines) == 3
