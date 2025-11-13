"""Blog content schemas."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class StyleProfile(BaseModel):
    """Style profile for content generation."""

    tone: Optional[str] = Field(
        None, description="e.g., professional, casual, humorous"
    )
    voice: Optional[str] = Field(
        None, description="e.g., authoritative, conversational"
    )
    length: Optional[str] = Field(None, description="e.g., short, medium, long")


class BlogGenerateRequest(BaseModel):
    """Request schema for blog generation."""

    topic: str = Field(..., min_length=1, max_length=500, description="Blog topic")
    style_profile: Optional[StyleProfile] = None
    keywords: Optional[List[str]] = Field(None, max_length=20)
    project_id: Optional[str] = Field(None, description="Project to save the blog to")


class BlogGenerateResponse(BaseModel):
    """Response schema for blog generation."""

    title: str
    content: str
    word_count: int
    metadata: Dict[str, Any]
    saved_item_id: Optional[str] = None


class OutlineGenerateRequest(BaseModel):
    """Request schema for outline generation."""

    topic: str = Field(..., min_length=1, max_length=500)
    sections: Optional[int] = Field(5, ge=1, le=20)
    project_id: Optional[str] = None


class OutlineGenerateResponse(BaseModel):
    """Response schema for outline generation."""

    topic: str
    sections: List[str]
    saved_item_id: Optional[str] = None
