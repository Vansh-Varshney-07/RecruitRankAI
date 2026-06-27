from ollama import Client

OLLAMA_HOST = "http://127.0.0.1:11434"
EMBEDDING_MODEL = "nomic-embed-text"

client = Client(host=OLLAMA_HOST)


def embed(text: str) -> list[float]:
    """
    Generate an embedding vector for the given text.
    """

    response = client.embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.embeddings[0]