from recruit_ai.job.parser import parse_job


def test_parse_job_handles_colons_bullets_and_aliases():
    job = parse_job(
        """
        Senior ML Engineer

        Required qualifications:
        - Python, SQL
        - Machine Learning; Deep Learning

        Nice to have:
        Docker
        Kubernetes

        Work experience:
        4+ years
        """
    )

    assert job.title == "Senior ML Engineer"
    assert job.required_skills == [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
    ]
    assert job.preferred_skills == [
        "Docker",
        "Kubernetes",
    ]
    assert job.experience == ["4+ years"]
