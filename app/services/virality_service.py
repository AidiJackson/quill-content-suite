"""Virality scoring and optimization service."""

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.virality_score import ViralityScore
from app.services.ai_client import AIClient

logger = get_logger(__name__)


class ViralityService:
    """Service for virality scoring and content optimization."""

    def __init__(self, ai_client: AIClient, db: Optional[Session] = None):
        """Initialize virality service."""
        self.ai_client = ai_client
        self.db = db

    def score_content(
        self, text: str, content_item_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Score content for virality potential."""
        logger.info("Scoring content for virality")

        score_data = self.ai_client.virality_score(text)

        saved_score_id = None
        if content_item_id and self.db:
            saved_score_id = self._save_virality_score(content_item_id, score_data)

        return {
            **score_data,
            "saved_score_id": saved_score_id,
        }

    def rewrite_for_virality(
        self, text: str, target_platform: Optional[str] = None
    ) -> Dict[str, Any]:
        """Rewrite content to maximize virality."""
        logger.info(f"Rewriting content for virality (platform: {target_platform})")

        # Get original score
        original_score_data = self.ai_client.virality_score(text)

        # Rewrite with virality-focused instructions
        platform_hint = f" for {target_platform}" if target_platform else ""
        instructions = f"Rewrite to maximize engagement and virality{platform_hint}. Focus on hooks, emotional triggers, and clear structure."

        rewritten_text = self.ai_client.rewrite(text, instructions)

        # Get improved score
        improved_score_data = self.ai_client.virality_score(rewritten_text)

        improvements = []
        if improved_score_data["hook_score"] > original_score_data["hook_score"]:
            improvements.append("Improved hook strength")
        if (
            improved_score_data["structure_score"]
            > original_score_data["structure_score"]
        ):
            improvements.append("Better content structure")
        if improved_score_data["niche_score"] > original_score_data["niche_score"]:
            improvements.append("More niche-relevant")

        return {
            "original_text": text,
            "rewritten_text": rewritten_text,
            "original_score": original_score_data["overall_score"],
            "improved_score": improved_score_data["overall_score"],
            "improvements": improvements,
        }

    def _save_virality_score(self, item_id: str, score_data: Dict[str, Any]) -> str:
        """Save virality score to database."""
        if not self.db:
            raise ValueError("Database session required to save score")

        score = ViralityScore(
            item_id=item_id,
            hook_score=score_data["hook_score"],
            structure_score=score_data["structure_score"],
            niche_score=score_data["niche_score"],
            predicted_engagement=score_data["predicted_engagement"],
        )

        self.db.add(score)
        self.db.commit()
        self.db.refresh(score)

        logger.info(f"Saved virality score: {score.id}")
        return score.id
