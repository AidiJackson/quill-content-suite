"""Content Project model."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.content_item import ContentItem
    from app.models.media_file import MediaFile


class ContentProject(Base, UUIDMixin, TimestampMixin):
    """Content project model for organizing content and media."""

    __tablename__ = "content_projects"

    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    content_items: Mapped[List["ContentItem"]] = relationship(
        "ContentItem", back_populates="project", cascade="all, delete-orphan"
    )
    media_files: Mapped[List["MediaFile"]] = relationship(
        "MediaFile", back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ContentProject(id={self.id}, title={self.title})>"
