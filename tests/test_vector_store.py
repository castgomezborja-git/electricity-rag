from datetime import datetime, timezone

import pytest

from electricity_rag.retrieval.vector_store import search_similar_chunks
from electricity_rag.models import Document, Chunk


QUERY_VECTOR = [1.0] + [0.0] * 383


def test_search_similar_chunks_orders_by_cosine_distance(db_session):
    doc = Document(
        title="Documento de prueba - distancia coseno",
        source="test",
        content_hash="test-hash-distancia-coseno",
        ingested_at=datetime.now(timezone.utc),
    )

    doc.chunks.append(Chunk(
        content="Chunk idéntico a la pregunta",
        chunk_index=0,
        token_count=10,
        embedding=[1.0] + [0.0] * 383,
    ))
    doc.chunks.append(Chunk(
        content="Chunk perpendicular a la pregunta",
        chunk_index=1,
        token_count=10,
        embedding=[0.0, 1.0] + [0.0] * 382,
    ))
    doc.chunks.append(Chunk(
        content="Chunk opuesto a la pregunta",
        chunk_index=2,
        token_count=10,
        embedding=[-1.0] + [0.0] * 383,
    ))

    db_session.add(doc)
    db_session.commit()

    results = search_similar_chunks("-", top_k=3, session=db_session, query_embedding=QUERY_VECTOR)

    # Assert
    assert len(results) == 3

    assert results[0].chunk_text == "Chunk idéntico a la pregunta"
    assert results[1].chunk_text == "Chunk perpendicular a la pregunta"
    assert results[2].chunk_text == "Chunk opuesto a la pregunta"

    assert results[0].distance == pytest.approx(0.0)
    assert results[1].distance == pytest.approx(1.0)
    assert results[2].distance == pytest.approx(2.0)