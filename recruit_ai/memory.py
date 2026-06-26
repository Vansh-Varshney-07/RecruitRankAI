from recruit_ai.chroma import client
import uuid


def get_collection(room: str, memory_type: str):
    name = f"{room}_{memory_type}"
    return client.get_or_create_collection(name=name)


def store(room: str, memory_type: str, text: str):
    collection = get_collection(room, memory_type)

    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[text],
    )


def recall(room: str, memory_type: str, query: str, n_results: int = 3):
    collection = get_collection(room, memory_type)

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    return results["documents"][0]