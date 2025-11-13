"""Virality scoring schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ViralityScoreRequest(BaseModel):
    """Request schema for virality scoring."""

    text: str = Field(..., min_length=1)
    content_item_id: Optional[str] = Field(None, description="Content item to score")


class ViralityScoreResponse(BaseModel):
    """Response schema for virality scoring."""

    hook_score: int = Field(..., ge=0, le=100)
    structure_score: int = Field(..., ge=0, le=100)
    niche_score: int = Field(..., ge=0, le=100)
    overall_score: int = Field(..., ge=0, le=100)
    predicted_engagement: float
    recommendations: List[str]
    saved_score_id: Optional[str] = None


class ViralityScoreDBResponse(BaseModel):
    """Database schema for virality score."""

    id: str
    item_id: str
    hook_score: int
    structure_score: int
    niche_score: int
    predicted_engagement: float
    created_at: datetime

    model_config = {"from_attributes": True}


class ViralityRewriteRequest(BaseModel):
    """Request schema for virality-focused rewriting."""

    text: str = Field(..., min_length=1)
    target_platform: Optional[str] = Field(None, description="e.g., twitter, linkedin")


class ViralityRewriteResponse(BaseModel):
    """Response schema for virality rewriting."""

    original_text: str
    rewritten_text: str
    original_score: int
    improved_score: int
    improvements: List[str]
