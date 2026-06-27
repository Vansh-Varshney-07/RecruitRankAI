from recruit_ai.candidate.schema import Project


PROJECT_HEADERS = [
    "projects",
    "projects & independent research",
]


def extract_projects(sections: dict) -> list[Project]:

    projects = []

    for header in PROJECT_HEADERS:

        if header not in sections:
            continue

        text = sections[header]

        for line in text.splitlines():

            line = line.strip()

            if len(line) < 5:
                continue

            if line.startswith("–"):
                continue

            if line.isupper():
                continue

            if "·" in line or "—" in line:

                projects.append(
                    Project(
                        title=line
                    )
                )

    return projects