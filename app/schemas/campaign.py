"""Campaign content schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class CampaignStep(BaseModel):
    """Single step in a campaign."""

    step_number: int
    subject: str
    content: str
    delay_days: int


class CampaignGenerateRequest(BaseModel):
    """Request schema for campaign generation."""

    goal: str = Field(..., min_length=1, max_length=500, description="Campaign goal")
    steps: int = Field(3, ge=1, le=10, description="Number of steps")
    audience: Optional[str] = Field(None, description="Target audience description")
    project_id: Optional[str] = None


class CampaignGenerateResponse(BaseModel):
    """Response schema for campaign generation."""

    goal: str
    audience: Optional[str]
    steps: List[CampaignStep]
    total_duration_days: int
    saved_item_id: Optional[str] = None


class ContentExpandRequest(BaseModel):
    """Request schema for content expansion."""

    text: str = Field(..., min_length=1)
    target_length: Optional[str] = Field(
        "double", description="short/medium/long/double"
    )


class ContentExpandResponse(BaseModel):
    """Response schema for content expansion."""

    original_length: int
    expanded_length: int
    content: str


class ContentShortenRequest(BaseModel):
    """Request schema for content shortening."""

    text: str = Field(..., min_length=1)
    target_length: Optional[int] = Field(None, ge=10)


class ContentShortenResponse(BaseModel):
    """Response schema for content shortening."""

    original_length: int
    shortened_length: int
    content: str


class ContentRewriteRequest(BaseModel):
    """Request schema for content rewriting."""

    text: str = Field(..., min_length=1)
    instructions: str = Field(..., min_length=1, max_length=500)


class ContentRewriteResponse(BaseModel):
    """Response schema for content rewriting."""

    original: str
    rewritten: str
