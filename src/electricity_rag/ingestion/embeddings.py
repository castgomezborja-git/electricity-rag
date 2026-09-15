from electricity_rag.embedding_model import embedding_model


def embed_chunks(texts: list[str]) -> list[list[float]]:
    embeddings = embedding_model.encode(texts)
    return embeddings.tolist()