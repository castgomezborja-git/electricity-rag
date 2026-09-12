from electricity_rag.db import Base, engine
from electricity_rag import models  # noqa: F401

Base.metadata.create_all(engine)