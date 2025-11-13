"""Social post content schemas."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Platform(str, Enum):
    """Social media platform enumeration."""

    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    REDDIT = "reddit"
    INSTAGRAM = "instagram"


class PostGenerateRequest(BaseModel):
    """Request schema for social post generation."""

    topic: str = Field(..., min_length=1, max_length=500)
    platforms: List[Platform] = Field(..., min_length=1)
    include_hooks: bool = Field(True, description="Include attention-grabbing hooks")
    project_id: Optional[str] = None


class SocialPost(BaseModel):
    """Individual social post."""

    platform: Platform
    content: str
    character_count: int
    hashtags: List[str]


class PostGenerateResponse(BaseModel):
    """Response schema for social post generation."""

    posts: List[SocialPost]
    saved_item_ids: Optional[List[str]] = None


class HookGenerateRequest(BaseModel):
    """Request schema for hook generation."""

    topic: str = Field(..., min_length=1, max_length=500)
    count: int = Field(5, ge=1, le=20)
    platform: Optional[Platform] = None


class HookGenerateResponse(BaseModel):
    """Response schema for hook generation."""

    hooks: List[str]
