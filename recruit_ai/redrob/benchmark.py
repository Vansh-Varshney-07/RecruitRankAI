from pathlib import Path

from recruit_ai.redrob.loader import load_candidates


DATASET = Path(
    "data/redrob/candidates.jsonl"
)


def main():

    for i, candidate in enumerate(load_candidates(DATASET)):

        print("=" * 40)
        print(f"Candidate #{i+1}")
        print("=" * 40)

        print(candidate)

        if i == 2:
            break


if __name__ == "__main__":
    main()