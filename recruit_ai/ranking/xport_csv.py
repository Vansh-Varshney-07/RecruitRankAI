import csv


def export_results(rankings, output_file):

    with open(output_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "Rank",
                "Candidate",
                "Overall Score",
                "Skill",
                "Education",
                "Experience",
                "Projects",
                "Research",
            ]
        )

        for rank, item in enumerate(rankings, start=1):

            score = item["breakdown"]

            writer.writerow(
                [
                    rank,
                    item["candidate"].name,
                    score["overall"],
                    score["skill"],
                    score["education"],
                    score["experience"],
                    score["projects"],
                    score["research"],
                ]
            )