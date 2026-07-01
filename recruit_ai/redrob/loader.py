import json
from pathlib import Path


def load_candidates(path: str | Path):
    """
    Stream candidates from a JSONL file or a JSON array file.
    """

    path = Path(path)

    if path.suffix.lower() == ".json":
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            data = data.get("candidates", [])

        for item in data:
            yield item

        return

    with open(path, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            yield json.loads(line)
