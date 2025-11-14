"""Media processing schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.media_file import MediaType


class MediaFileBase(BaseModel):
    """Base schema for media file."""

    url: str = Field(..., min_length=1, max_length=2000)
    type: MediaType
    metadata: Optional[Dict[str, Any]] = None


class MediaFileCreate(MediaFileBase):
    """Schema for creating a media file."""

    project_id: str


class MediaFileResponse(MediaFileBase):
    """Schema for media file response."""

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Video Processing Schemas
class VideoTrimRequest(BaseModel):
    """Request schema for video trimming."""

    input_url: str = Field(..., min_length=1)
    start_time: float = Field(..., ge=0, description="Start time in seconds")
    end_time: float = Field(..., gt=0, description="End time in seconds")
    project_id: Optional[str] = None


class VideoTrimResponse(BaseModel):
    """Response schema for video trimming."""

    output_url: str
    duration: float
    saved_media_id: Optional[str] = None


class VideoCaptionsRequest(BaseModel):
    """Request schema for video captions."""

    input_url: str = Field(..., min_length=1)


class VideoCaptionsResponse(BaseModel):
    """Response schema for video captions."""

    srt_content: str
    caption_count: int


class VideoResizeRequest(BaseModel):
    """Request schema for video resizing."""

    input_url: str = Field(..., min_length=1)
    aspect_ratio: str = Field(..., description="e.g., 16:9, 9:16, 1:1")
    project_id: Optional[str] = None


class VideoResizeResponse(BaseModel):
    """Response schema for video resizing."""

    output_url: str
    aspect_ratio: str
    saved_media_id: Optional[str] = None


class VideoShortsRequest(BaseModel):
    """Request schema for generating shorts."""

    input_url: str = Field(..., min_length=1)
    count: int = Field(3, ge=1, le=10)
    project_id: Optional[str] = None


class VideoShortsResponse(BaseModel):
    """Response schema for generating shorts."""

    clips: List[Dict[str, Any]]
    saved_media_ids: Optional[List[str]] = None


# Audio Processing Schemas
class AudioCleanupRequest(BaseModel):
    """Request schema for audio cleanup."""

    input_url: str = Field(..., min_length=1)
    project_id: Optional[str] = None


class AudioCleanupResponse(BaseModel):
    """Response schema for audio cleanup."""

    output_url: str
    saved_media_id: Optional[str] = None


class AudioPitchShiftRequest(BaseModel):
    """Request schema for audio pitch shifting."""

    input_url: str = Field(..., min_length=1)
    semitones: int = Field(..., ge=-12, le=12)
    project_id: Optional[str] = None


class AudioPitchShiftResponse(BaseModel):
    """Response schema for audio pitch shifting."""

    output_url: str
    semitones: int
    saved_media_id: Optional[str] = None


class AudioTempoShiftRequest(BaseModel):
    """Request schema for audio tempo shifting."""

    input_url: str = Field(..., min_length=1)
    percent: int = Field(
        ..., ge=50, le=200, description="Tempo percentage (100 = no change)"
    )
    project_id: Optional[str] = None


class AudioTempoShiftResponse(BaseModel):
    """Response schema for audio tempo shifting."""

    output_url: str
    tempo_percent: int
    saved_media_id: Optional[str] = None


class AudioExtractRequest(BaseModel):
    """Request schema for audio extraction from video."""

    input_url: str = Field(..., min_length=1)
    project_id: Optional[str] = None


class AudioExtractResponse(BaseModel):
    """Response schema for audio extraction."""

    output_url: str
    duration: float
    saved_media_id: Optional[str] = None


# AI Video Generation Schemas (Stub)
class AIVideoGenerateRequest(BaseModel):
    """Request schema for AI video generation."""

    prompt: str = Field(..., min_length=1, max_length=1000)
    style: Optional[str] = Field(None, description="Video style (e.g., realistic, animated)")
    duration: Optional[int] = Field(30, ge=5, le=300, description="Duration in seconds")
    project_id: Optional[str] = None


class AIVideoGenerateResponse(BaseModel):
    """Response schema for AI video generation."""

    video_url: str
    duration: int
    metadata: Dict[str, Any]
    saved_media_id: Optional[str] = None


# Music Generation Schemas
class VocalStyle(BaseModel):
    """Vocal style configuration."""

    gender: str = Field(..., description="Vocal gender: male, female, mixed, auto")
    tone: str = Field(..., description="Vocal tone: emotional, aggressive, smooth, etc.")
    energy: str = Field(..., description="Energy level: low, medium, high")


class MusicSection(BaseModel):
    """Song section structure."""

    name: str = Field(..., description="Section name (e.g., Intro, Verse 1, Chorus)")
    bars: int = Field(..., ge=1, le=64, description="Number of bars in this section")
    description: str = Field(..., description="Musical description of what happens")
    lyrics: str = Field(..., description="Lyrics for this section")


class MusicGenerateRequest(BaseModel):
    """Request schema for music generation."""

    genre: str = Field(..., description="Music genre (e.g., trap, drill, afrobeat, lofi, pop, edm, rnb, hiphop)")
    mood: str = Field(..., description="Mood (e.g., dark, energetic, emotional, dreamy, uplifting, chill)")
    tempo_bpm: Optional[int] = Field(None, ge=60, le=200, description="Tempo in BPM")
    reference_text: Optional[str] = Field(None, description="Reference text or song idea")
    sections: Optional[List[str]] = Field(None, description="Desired sections (e.g., intro, verse, chorus)")
    project_id: Optional[str] = None


class MusicGenerateResponse(BaseModel):
    """Response schema for music generation."""

    track_id: str = Field(..., description="Unique track identifier")
    title: str = Field(..., description="Generated song title")
    genre: str
    mood: str
    tempo_bpm: Optional[int] = None
    vocal_style: VocalStyle
    hook: str = Field(..., description="Memorable hook line")
    chorus: str = Field(..., description="Main chorus lyrics")
    sections: List[MusicSection] = Field(..., description="Song structure with lyrics")
    fake_audio_url: str = Field(..., description="Placeholder audio URL")
    saved_media_id: Optional[str] = None


# Vocal Generation Schemas
class VocalGenerateRequest(BaseModel):
    """Request schema for vocal generation."""

    track_id: Optional[str] = Field(None, description="Associated track ID")
    lyrics: str = Field(..., min_length=1, description="Lyrics to sing")
    vocal_style: VocalStyle = Field(..., description="Vocal style configuration")
    tempo_bpm: Optional[int] = Field(None, ge=60, le=200, description="Tempo in BPM")
    reference_text: Optional[str] = Field(None, description="Reference or context for vocal generation")


class VocalGenerateResponse(BaseModel):
    """Response schema for vocal generation."""

    vocal_id: str = Field(..., description="Unique vocal rendering ID")
    track_id: Optional[str] = Field(None, description="Associated track ID")
    audio_url: str = Field(..., description="URL to generated audio file")
    duration_seconds: Optional[int] = Field(None, description="Duration in seconds")
    vocal_style: VocalStyle = Field(..., description="Vocal style used")
    notes: Optional[str] = Field(None, description="Generation notes or metadata")
