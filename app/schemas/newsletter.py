"""Newsletter content schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class NewsletterSection(BaseModel):
    """Newsletter section."""

    heading: str
    content: str


class NewsletterGenerateRequest(BaseModel):
    """Request schema for newsletter generation."""

    subject: str = Field(..., min_length=1, max_length=500)
    topics: List[str] = Field(..., min_length=1, max_length=10)
    tone: Optional[str] = Field("professional", description="Newsletter tone")
    project_id: Optional[str] = None


class NewsletterGenerateResponse(BaseModel):
    """Response schema for newsletter generation."""

    subject: str
    preview_text: str
    sections: List[NewsletterSection]
    cta: str
    word_count: int
    saved_item_id: Optional[str] = None
