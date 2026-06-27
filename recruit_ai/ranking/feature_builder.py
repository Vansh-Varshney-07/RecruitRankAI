from recruit_ai.candidate.schema import CandidateProfile


def build_candidate_features(candidate: CandidateProfile) -> dict:
    """
    Convert a CandidateProfile into a feature dictionary.
    """

    return {
        "skills": candidate.skills,
        "education": candidate.education,
        "experience": candidate.experience,
        "projects": candidate.projects,
        "certifications": candidate.certifications,
        "research_interests": candidate.research_interests,
    }