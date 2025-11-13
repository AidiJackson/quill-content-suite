"""Audio processing routes."""

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.schemas.media import (AudioCleanupRequest, AudioCleanupResponse,
                               AudioExtractRequest, AudioExtractResponse,
                               AudioPitchShiftRequest, AudioPitchShiftResponse,
                               AudioTempoShiftRequest, AudioTempoShiftResponse)
from app.services.audio_service import AudioService

router = APIRouter(prefix="/audio", tags=["Audio Processing"])


@router.post("/cleanup", response_model=AudioCleanupResponse)
def cleanup_audio(
    request: AudioCleanupRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Clean up audio (noise reduction)."""
    service = AudioService(db)

    result = service.cleanup_audio(
        input_url=request.input_url,
        project_id=request.project_id,
    )

    return result


@router.post("/pitch", response_model=AudioPitchShiftResponse)
def pitch_shift(
    request: AudioPitchShiftRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Shift audio pitch."""
    service = AudioService(db)

    result = service.pitch_shift(
        input_url=request.input_url,
        semitones=request.semitones,
        project_id=request.project_id,
    )

    return result


@router.post("/tempo", response_model=AudioTempoShiftResponse)
def tempo_shift(
    request: AudioTempoShiftRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Shift audio tempo."""
    service = AudioService(db)

    result = service.tempo_shift(
        input_url=request.input_url,
        percent=request.percent,
        project_id=request.project_id,
    )

    return result


@router.post("/extract", response_model=AudioExtractResponse)
def extract_audio(
    request: AudioExtractRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Extract audio from video."""
    service = AudioService(db)

    result = service.extract_audio(
        input_url=request.input_url,
        project_id=request.project_id,
    )

    return result
