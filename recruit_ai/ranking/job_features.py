from recruit_ai.job.schema import JobProfile


def build_job_features(job: JobProfile) -> dict:
    """
    Convert a JobProfile into a feature dictionary.
    """

    return {
        "required_skills": job.required_skills,
        "preferred_skills": job.preferred_skills,
        "education": job.education,
        "experience": job.experience,
    }