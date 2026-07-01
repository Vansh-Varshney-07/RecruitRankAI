from recruit_ai.candidate.schema import (
    CandidateProfile,
    Skill,
    Education,
    Experience,
    Project,
    Certification,
)


def build_candidate(candidate_json: dict) -> CandidateProfile:

    profile = CandidateProfile()
    profile_data = candidate_json.get("profile", {})

    profile.candidate_id = candidate_json.get("candidate_id", "")

    profile.name = profile_data.get(
        "anonymized_name",
        ""
    )

    profile.headline = profile_data.get("headline", "")
    profile.location = profile_data.get("location", "")
    profile.years_of_experience = float(
        profile_data.get("years_of_experience", 0.0) or 0.0
    )
    profile.signals = candidate_json.get("redrob_signals", {})

    profile.raw_text = profile_data.get(
        "summary",
        ""
    )

    # -----------------------
    # Skills
    # -----------------------

    for skill in candidate_json.get("skills", []):

        if isinstance(skill, dict):
            skill_name = skill.get("name", "")
            proficiency = skill.get("proficiency", "")
            endorsements = int(skill.get("endorsements", 0) or 0)
            duration_months = int(skill.get("duration_months", 0) or 0)
        else:
            skill_name = str(skill)
            proficiency = ""
            endorsements = 0
            duration_months = 0

        profile.skills.append(
            Skill(
                name=skill_name,
                proficiency=proficiency,
                endorsements=endorsements,
                duration_months=duration_months,
            )
        )
    # -----------------------
    # Education
    # -----------------------

    for edu in candidate_json.get("education", []):

        profile.education.append(
            Education(
                degree=edu.get("degree", ""),
                institute=edu.get("institution", ""),
                year=str(edu.get("end_year", "")),
                field_of_study=edu.get("field_of_study", ""),
            )
        )

    # -----------------------
    # Experience
    # -----------------------

    for exp in candidate_json.get("career_history", []):

        profile.experience.append(
            Experience(
                title=exp.get("title", ""),
                company=exp.get("company", ""),
                duration=f"{round((exp.get('duration_months', 0) or 0) / 12, 1)} years",
                duration_months=int(exp.get("duration_months", 0) or 0),
                description=exp.get("description", ""),
                is_current=bool(exp.get("is_current", False)),
            )
        )

    # -----------------------
    # Projects
    # -----------------------

    for project in candidate_json.get("projects", []):

        profile.projects.append(
            Project(
                title=project.get("title", ""),
                summary=project.get("description", ""),
                technologies=[],
            )
        )

    # -----------------------
    # Certifications
    # -----------------------

    for cert in candidate_json.get("certifications", []):
        if isinstance(cert, dict):
            cert_name = cert.get("name", "")
            provider = cert.get("issuer", "")
        else:
            cert_name = str(cert)
            provider = ""

        profile.certifications.append(
            Certification(
                name=cert_name,
                provider=provider,
            )
        )

    return profile
