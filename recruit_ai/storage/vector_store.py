import uuid

from recruit_ai.embeddings.embedder import embed
from recruit_ai.storage.chroma import client


def get_collection(collection_name: str):
    """
    Create (or retrieve) a ChromaDB collection.
    """
    return client.get_or_create_collection(
        name=collection_name
    )


def add_document(
    collection_name: str,
    document: str,
    embedding: list,
    metadata: dict,
):
    """
    Store a document together with its embedding and metadata.
    """
    collection = get_collection(collection_name)

    kwargs = {
        "ids": [str(uuid.uuid4())],
        "documents": [document],
        "embeddings": [embedding],
    }

    # Add metadata only if provided
    if metadata:
        kwargs["metadatas"] = [metadata]

    collection.add(**kwargs)


def search(
    collection_name: str,
    query: str,
    n_results: int = 5,
):
    """
    Perform semantic search using Ollama embeddings.
    """
    collection = get_collection(collection_name)

    query_embedding = embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    return results