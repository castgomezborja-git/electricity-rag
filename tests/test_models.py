from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from electricity_rag.models import Document, Chunk


def test_document_title_must_be_unique(db_session):
    # Arrange
    doc1 = Document(
        title="Documento único",
        source="test",
        content_hash="hash-1",
        ingested_at=datetime.now(timezone.utc),
    )
    db_session.add(doc1)
    db_session.commit()

    doc2 = Document(
        title="Documento único",  # mismo título, hash distinto
        source="test",
        content_hash="hash-2",
        ingested_at=datetime.now(timezone.utc),
    )
    db_session.add(doc2)

    # Act / Assert
    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_deleting_document_cascades_to_chunks(db_session):
    # Arrange
    doc = Document(
        title="Documento con chunks",
        source="test",
        content_hash="hash-cascade",
        ingested_at=datetime.now(timezone.utc),
    )
    doc.chunks.append(Chunk(
        content="Chunk 1",
        chunk_index=0,
        token_count=5,
        embedding=[0.0] * 384,
    ))
    doc.chunks.append(Chunk(
        content="Chunk 2",
        chunk_index=1,
        token_count=5,
        embedding=[0.0] * 384,
    ))
    db_session.add(doc)
    db_session.commit()
    document_id = doc.id

    # Act
    db_session.delete(doc)
    db_session.commit()

    # Assert
    remaining_chunks = db_session.query(Chunk).filter_by(document_id=document_id).all()
    assert remaining_chunks == []