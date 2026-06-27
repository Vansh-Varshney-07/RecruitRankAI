from pathlib import Path

from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.ingestion.preprocess import clean_text
from recruit_ai.embeddings.embedder import embed
from recruit_ai.storage.vector_store import add_document


def ingest_resume(pdf_path: str, collection_name: str = "candidates"):
    """
    Ingest a single resume into ChromaDB.
    """

    pdf = Path(pdf_path)

    print(f"Processing: {pdf.name}")

    # Extract
    text = extract_text(str(pdf))

    # Clean
    text = clean_text(text)

    # Generate embedding
    embedding = embed(text)

    # Metadata
    metadata = {
        "filename": pdf.name,
        "candidate_id": pdf.stem,
        "source": "resume",
    }

    # Store
    add_document(
        collection_name=collection_name,
        document=text,
        embedding=embedding,
        metadata=metadata,
    )

    print("Stored successfully.")