import math

from recruit_ai.embeddings.embedder import embed


def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors.
    """

    dot = sum(a * b for a, b in zip(vec1, vec2))

    norm1 = math.sqrt(sum(a * a for a in vec1))

    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


def semantic_similarity(text1: str, text2: str) -> float:

    emb1 = embed(text1)

    emb2 = embed(text2)

    return cosine_similarity(
        emb1,
        emb2,
    )