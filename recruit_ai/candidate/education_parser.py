from recruit_ai.candidate.schema import Education


EDUCATION_HEADERS = [
    "education",
]


def extract_education(sections: dict) -> list[Education]:

    education = []

    for header in EDUCATION_HEADERS:

        if header not in sections:
            continue

        text = sections[header]

        for line in text.splitlines():

            line = line.strip()

            if len(line) < 3:
                continue

            education.append(
                Education(
                    degree=line
                )
            )

    return education