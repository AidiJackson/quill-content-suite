"""Media File model."""

import enum
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import JSON, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.content_project import ContentProject


class MediaType(str, enum.Enum):
    """Media type enumeration."""

    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


class MediaFile(Base, UUIDMixin, TimestampMixin):
    """Media file model for storing media references."""

    __tablename__ = "media_files"

    project_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("content_projects.id"), nullable=False, index=True
    )
    url: Mapped[str] = mapped_column(String(2000), nullable=False)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False, index=True)
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    project: Mapped["ContentProject"] = relationship(
        "ContentProject", back_populates="media_files"
    )

    def __repr__(self) -> str:
        return f"<MediaFile(id={self.id}, type={self.type}, url={self.url[:50]})>"
