from recruit_ai.candidate.schema import ResearchInterest


def extract_research(sections: dict) -> list[ResearchInterest]:

    if "research interests" not in sections:
        return []

    text = sections["research interests"]

    text = text.replace("•", ",")

    interests = []

    for item in text.split(","):

        item = item.strip()

        if not item:
            continue

        interests.append(
            ResearchInterest(
                topic=item
            )
        )

    return interests