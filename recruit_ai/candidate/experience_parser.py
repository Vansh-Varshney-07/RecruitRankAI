from recruit_ai.candidate.schema import Experience


def extract_experience(sections: dict) -> list[Experience]:

    if "experience" not in sections:
        return []

    experience = []

    for line in sections["experience"].splitlines():

        line = line.strip()

        if not line:
            continue

        experience.append(
            Experience(
                title=line
            )
        )

    return experience