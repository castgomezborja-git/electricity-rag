from dataclasses import dataclass

from electricity_rag.db import SessionLocal
from electricity_rag.models import Chunk
from electricity_rag.ingestion.embeddings import embed_chunks

@dataclass
class SearchResult:
    document_title: str
    document_source: str
    chunk_text: str
    distance: float

def search_similar_chunks(query: str, top_k: int = 5) -> list[SearchResult]:
    query_embedding = embed_chunks([query])[0]

    with SessionLocal() as session:
        results = (
            session.query(Chunk, Chunk.embedding.cosine_distance(query_embedding).label("distance"))
            .order_by(Chunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
            .all()
        )
        return [SearchResult(document_title=chunk.document.title, document_source=chunk.document.source, chunk_text=chunk.content, distance=distance) for chunk, distance in results]