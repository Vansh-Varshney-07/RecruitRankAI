import csv


def export_results(results,path):

    with open(path,"w",newline="",encoding="utf8") as f:

        writer=csv.writer(f)

        writer.writerow([
            "Rank",
            "Candidate",
            "Overall",
            "Skill",
            "Semantic",
            "Experience",
            "Education",
            "Projects"
        ])

        for i,item in enumerate(results,1):

            s=item["breakdown"]

            writer.writerow([

                i,

                item["candidate"].name,

                s["overall"],

                s["skill"],

                s["semantic"],

                s["experience"],

                s["education"],

                s["projects"]

            ])