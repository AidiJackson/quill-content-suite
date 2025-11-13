"""Virality scoring and optimization routes."""

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.schemas.virality import (ViralityRewriteRequest,
                                  ViralityRewriteResponse,
                                  ViralityScoreRequest, ViralityScoreResponse)
from app.services.ai_client import get_ai_client
from app.services.virality_service import ViralityService

router = APIRouter(prefix="/virality", tags=["Virality"])


@router.post("/score", response_model=ViralityScoreResponse)
def score_content(
    request: ViralityScoreRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Score content for virality potential."""
    ai_client = get_ai_client()
    service = ViralityService(ai_client, db)

    result = service.score_content(
        text=request.text,
        content_item_id=request.content_item_id,
    )

    return result


@router.post("/rewrite", response_model=ViralityRewriteResponse)
def rewrite_for_virality(
    request: ViralityRewriteRequest,
    current_user: CurrentUser,
):
    """Rewrite content to maximize virality."""
    ai_client = get_ai_client()
    service = ViralityService(ai_client)

    result = service.rewrite_for_virality(
        text=request.text,
        target_platform=request.target_platform,
    )

    return result
