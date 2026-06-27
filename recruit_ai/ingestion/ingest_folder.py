from pathlib import Path

from recruit_ai.ingestion.ingest_resume import ingest_resume


RESUME_FOLDER = Path("data/raw/resumes")


def ingest_all():
    pdfs = sorted(RESUME_FOLDER.glob("*.pdf"))

    if not pdfs:
        print("No PDF resumes found.")
        return

    print(f"\nFound {len(pdfs)} resumes.\n")

    success = 0

    for i, pdf in enumerate(pdfs, start=1):
        try:
            print(f"[{i}/{len(pdfs)}] {pdf.name}")

            ingest_resume(str(pdf))

            success += 1

        except Exception as e:
            print(f"Failed: {pdf.name}")
            print(e)

    print("\n==============================")
    print("Batch ingestion complete")
    print(f"Indexed {success}/{len(pdfs)} resumes.")
    print("==============================")


if __name__ == "__main__":
    ingest_all()