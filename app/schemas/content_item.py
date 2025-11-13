"""Content Item schemas."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.models.content_item import ContentType


class ContentItemBase(BaseModel):
    """Base schema for content item."""

    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    type: ContentType
    metadata: Optional[Dict[str, Any]] = None


class ContentItemCreate(ContentItemBase):
    """Schema for creating a content item."""

    project_id: str


class ContentItemUpdate(BaseModel):
    """Schema for updating a content item."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=1)
    metadata: Optional[Dict[str, Any]] = None


class ContentItemResponse(ContentItemBase):
    """Schema for content item response."""

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
