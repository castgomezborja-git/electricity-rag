import sys
from datetime import datetime, timezone

from electricity_rag.auth import hash_password
from electricity_rag.db import SessionLocal
from electricity_rag.models import User


def create_user(username: str, plain_password: str) -> None:
    with SessionLocal() as session:
        existing = session.query(User).filter_by(username=username).first()
        if existing is not None:
            print(f"El usuario '{username}' ya existe.")
            return

        user = User(
            username=username,
            hashed_password=hash_password(plain_password),
            created_at=datetime.now(timezone.utc),
        )
        session.add(user)
        session.commit()
        print(f"Usuario '{username}' creado.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: uv run python scripts/create_user.py <username> <password>")
        sys.exit(1)

    create_user(sys.argv[1], sys.argv[2])