from ui.dashboard import _job_text_from_upload
from ui.dashboard import _matches_query

from recruit_ai.candidate.schema import CandidateProfile, Skill


class FakeUpload:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self._content = content

    def getvalue(self) -> bytes:
        return self._content


def test_txt_job_upload_decodes_utf8_sig():
    upload = FakeUpload(
        "job.txt",
        "Machine Learning Engineer\n\nREQUIRED SKILLS\n\nPython".encode("utf-8-sig"),
    )

    assert _job_text_from_upload(upload).startswith("Machine Learning Engineer")


def test_unsupported_job_upload_raises_clear_error():
    upload = FakeUpload("job.docx", b"not supported")

    try:
        _job_text_from_upload(upload)
    except ValueError as error:
        assert "Unsupported job description format" in str(error)
    else:
        raise AssertionError("Expected unsupported upload to raise ValueError")


def test_result_query_matches_candidate_skills_and_location():
    item = {
        "candidate": CandidateProfile(
            name="Asha Rao",
            headline="ML Engineer",
            location="Bengaluru",
            skills=[
                Skill("PyTorch"),
            ],
        )
    }

    assert _matches_query(item, "pytorch")
    assert _matches_query(item, "bengaluru")
    assert not _matches_query(item, "sales")
