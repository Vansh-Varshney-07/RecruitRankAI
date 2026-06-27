import chromadb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "chroma"

client = chromadb.PersistentClient(path=str(DB_PATH))