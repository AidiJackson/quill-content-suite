"""Content Version model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.content_item import ContentItem


class ContentVersion(Base):
    """Content version model for tracking content history."""

    __tablename__ = "content_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("content_items.id"), nullable=False, index=True
    )
    version_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    item: Mapped["ContentItem"] = relationship("ContentItem", back_populates="versions")

    def __repr__(self) -> str:
        return f"<ContentVersion(id={self.id}, item_id={self.item_id}, version={self.version_index})>"
