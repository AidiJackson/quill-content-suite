"""Content Item model."""

import enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.content_project import ContentProject
    from app.models.version import ContentVersion
    from app.models.virality_score import ViralityScore


class ContentType(str, enum.Enum):
    """Content type enumeration."""

    BLOG = "blog"
    NEWSLETTER = "newsletter"
    POST = "post"
    SCRIPT = "script"
    IDEA = "idea"
    OUTLINE = "outline"
    CAMPAIGN = "campaign"
    HOOK = "hook"


class ContentItem(Base, UUIDMixin, TimestampMixin):
    """Content item model for storing generated content."""

    __tablename__ = "content_items"

    project_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("content_projects.id"), nullable=False, index=True
    )
    type: Mapped[ContentType] = mapped_column(
        Enum(ContentType), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    project: Mapped["ContentProject"] = relationship(
        "ContentProject", back_populates="content_items"
    )
    versions: Mapped[List["ContentVersion"]] = relationship(
        "ContentVersion", back_populates="item", cascade="all, delete-orphan"
    )
    virality_scores: Mapped[List["ViralityScore"]] = relationship(
        "ViralityScore", back_populates="item", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ContentItem(id={self.id}, type={self.type}, title={self.title})>"
