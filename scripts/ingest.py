from pathlib import Path

from electricity_rag.db import SessionLocal
from electricity_rag.hashing import compute_content_hash
from electricity_rag.ingestion.chunking import chunk_text
from electricity_rag.ingestion.embeddings import embed_chunks
from electricity_rag.ingestion.loaders import load_pdf
from electricity_rag.models import Chunk, Document
from datetime import datetime, timezone

DOCUMENTS_TO_INGEST = {
    "data/raw/cnmc_guia_consumidores_electricidad_2022.pdf": "Guía informativa CNMC 2022",
    "data/raw/omie_funcionamiento_mercado_diario.pdf": "Funcionamiento del Mercado Diario (OMIE)",
}


def ingest_document(path: str, title: str) -> None:
    loaded = load_pdf(path, title=title)
    content_hash = compute_content_hash(loaded.text)

    with SessionLocal() as session:
        existing = session.query(Document).filter_by(title=title).first()

        if existing is not None:
            if existing.content_hash == content_hash:
                print(f"[SIN CAMBIOS] {title}")
                return
            print(f"[ACTUALIZANDO] {title}")
            session.delete(existing)
            session.commit()
        else:
            print(f"[NUEVO] {title}")

        chunks = chunk_text(loaded.text)
        embeddings = embed_chunks([chunk.content for chunk in chunks])

        document = Document(
            title=title,
            source=path,
            content_hash=content_hash,
            ingested_at=datetime.now(timezone.utc),
        )

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            document.chunks.append(
                Chunk(
                    content=chunk.content,
                    chunk_index=index,
                    token_count=chunk.token_count,
                    embedding=embedding,
                )
            )

        session.add(document)
        session.commit()
        print(f"  -> {len(chunks)} chunks insertados")


if __name__ == "__main__":
    for path, title in DOCUMENTS_TO_INGEST.items():
        if not Path(path).exists():
            print(f"[AVISO] No existe el archivo: {path}")
            continue
        ingest_document(path, title)