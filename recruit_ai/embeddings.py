from ollama import Client

client = Client(host="http://127.0.0.1:11434")


def embed(text: str):
    response = client.embed(
        model="nomic-embed-text",
        input=text,
    )
    return response.embeddings[0]