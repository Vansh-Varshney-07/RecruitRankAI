from recruit_ai.candidate.schema import Certification


def extract_certifications(sections: dict) -> list[Certification]:

    if "certifications" not in sections:
        return []

    text = sections["certifications"]

    text = text.replace("•", ",")

    certifications = []

    for item in text.split(","):

        item = item.strip("– ").strip()

        if not item:
            continue

        certifications.append(
            Certification(
                name=item
            )
        )

    return certifications