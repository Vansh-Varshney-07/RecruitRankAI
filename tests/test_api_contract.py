from recruit_ai.api.server import RankRequest


def test_rank_request_defaults_are_demo_safe():
    request = RankRequest()

    assert request.scan_limit == 1000
    assert request.top_n == 25
    assert request.use_llm is False


def test_rank_request_accepts_llm_review_options():
    request = RankRequest(
        job_text="ML Engineer",
        scan_limit=50,
        top_n=5,
        use_llm=True,
        llm_limit=3,
    )

    assert request.job_text == "ML Engineer"
    assert request.use_llm is True
    assert request.llm_limit == 3
