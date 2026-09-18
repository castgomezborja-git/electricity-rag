from dataclasses import dataclass

from sqlalchemy.orm import Session

from electricity_rag.db import SessionLocal
from electricity_rag.models import Chunk
from electricity_rag.ingestion.embeddings import embed_chunks


@dataclass
class SearchResult:
    document_title: str
    document_source: str
    chunk_text: str
    distance: float


def search_similar_chunks(
    query: str,
    top_k: int = 5,
    session: Session | None = None,
    query_embedding: list[float] | None = None,
) -> list[SearchResult]:
    if query_embedding is None:
        query_embedding = embed_chunks([query])[0]

    owns_session = session is None
    if owns_session:
        session = SessionLocal()

    try:
        results = (
            session.query(Chunk, Chunk.embedding.cosine_distance(query_embedding).label("distance"))
            .order_by(Chunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
            .all()
        )
        return [
            SearchResult(
                document_title=chunk.document.title,
                document_source=chunk.document.source,
                chunk_text=chunk.content,
                distance=distance,
            )
            for chunk, distance in results
        ]
    finally:
        if owns_session:
            session.close()