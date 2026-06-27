from recruit_ai.embeddings.embedder import embed
from recruit_ai.storage.vector_store import get_collection


def semantic_search(
    query: str,
    collection_name: str = "candidates",
    n_results: int = 5,
):
    """
    Perform semantic similarity search.
    """

    collection = get_collection(collection_name)

    query_embedding = embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    return results
