import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from testcontainers.community.postgres import PostgresContainer

from electricity_rag.db import Base
from electricity_rag import models  # noqa: F401


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("pgvector/pgvector:pg16", driver="psycopg") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def db_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()
    with db_engine.connect() as conn:
        conn.execute(text("TRUNCATE documents, chunks, users RESTART IDENTITY CASCADE;"))
        conn.commit()