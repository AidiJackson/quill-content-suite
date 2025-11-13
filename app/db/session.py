"""Database session management."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in settings.database_url else {}
    ),
    echo=settings.debug and settings.is_development,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
