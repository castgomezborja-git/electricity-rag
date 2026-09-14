from electricity_rag.ingestion.chunking import chunk_text


def test_chunk_text_merges_small_final_chunk():
    # Arrange
    texto = "palabra " * 210  # genera ~212 tokens con cl100k_base

    # Act
    chunks = chunk_text(texto)

    # Assert
    assert len(chunks) == 1
    assert chunks[0].token_count == 212


def test_chunk_text_keeps_substantial_final_chunk_separate():
    # Arrange
    texto = "palabra " * 416  # genera ~420 tokens con cl100k_base

    # Act
    chunks = chunk_text(texto)

    # Assert
    assert len(chunks) == 3
    assert chunks[-1].token_count == 78


def test_chunk_overlap_must_be_smaller_than_chunk_size():
    # Arrange / Act / Assert
    import pytest
    with pytest.raises(ValueError):
        chunk_text("cualquier texto", chunk_size=100, chunk_overlap=100)