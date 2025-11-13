"""Virality Score model."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.content_item import ContentItem


class ViralityScore(Base, UUIDMixin, TimestampMixin):
    """Virality score model for content engagement predictions."""

    __tablename__ = "virality_scores"

    item_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("content_items.id"), nullable=False, index=True
    )
    hook_score: Mapped[int] = mapped_column(Integer, nullable=False)
    structure_score: Mapped[int] = mapped_column(Integer, nullable=False)
    niche_score: Mapped[int] = mapped_column(Integer, nullable=False)
    predicted_engagement: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    item: Mapped["ContentItem"] = relationship(
        "ContentItem", back_populates="virality_scores"
    )

    @property
    def overall_score(self) -> int:
        """Calculate overall virality score (0-100)."""
        return int((self.hook_score + self.structure_score + self.niche_score) / 3)

    def __repr__(self) -> str:
        return f"<ViralityScore(id={self.id}, overall={self.overall_score})>"
