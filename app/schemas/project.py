"""Content Project schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContentProjectBase(BaseModel):
    """Base schema for content project."""

    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None


class ContentProjectCreate(ContentProjectBase):
    """Schema for creating a content project."""

    user_id: str = Field(..., min_length=1, max_length=255)


class ContentProjectUpdate(BaseModel):
    """Schema for updating a content project."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None


class ContentProjectResponse(ContentProjectBase):
    """Schema for content project response."""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
