from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from electricity_rag.db import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    source: Mapped[str]
    content_hash: Mapped[str] = mapped_column(unique=True)
    ingested_at: Mapped[datetime]
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r}, source={self.source!r}, content_hash={self.content_hash!r}, ingested_at={self.ingested_at!r})"

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    document: Mapped[Document] = relationship(back_populates="chunks")
    content: Mapped[str]
    chunk_index: Mapped[int]
    token_count: Mapped[int]
    embedding: Mapped[list[float]] = mapped_column(Vector(384))
    

    def __repr__(self) -> str:
        return f"Chunk(id={self.id!r}, document_id={self.document_id!r}, content={self.content!r}, chunk_index={self.chunk_index!r}, token_count={self.token_count!r}, embedding={self.embedding!r})"