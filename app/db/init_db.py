"""Database initialization utilities."""

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.base import Base
from app.db.session import engine
# Import models to ensure they are registered
from app.models import (ContentItem, ContentProject,  # noqa: F401
                        ContentVersion, MediaFile, ViralityScore)

logger = get_logger(__name__)


def init_db() -> None:
    """Initialize database tables."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


def drop_db() -> None:
    """Drop all database tables (use with caution)."""
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.warning("Database tables dropped")
