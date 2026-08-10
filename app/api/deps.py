# Shared FastAPI dependencies.
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.postgres import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield one DB session per request and always close it afterwards, even on error."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
