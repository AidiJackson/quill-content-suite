"""Music generation routes."""

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.schemas.media import MusicGenerateRequest, MusicGenerateResponse
from app.services.music_service import MusicService

router = APIRouter(prefix="/music", tags=["Music Studio"])


@router.post("/generate", response_model=MusicGenerateResponse)
def generate_music_track(
    request: MusicGenerateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Generate a structured song with lyrics and sections.

    Creates a complete song blueprint including:
    - Title and metadata
    - Vocal style
    - Hook and chorus
    - Full song structure with lyrics for each section
    - Fake audio URL for future playback
    """
    service = MusicService(db)
    result = service.generate_song(request)
    return result


@router.post("/magic", response_model=MusicGenerateResponse)
async def magic_track(
    request: MusicGenerateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Generate an AI-enhanced magic track.

    This endpoint uses the "AI Producer" pipeline:
    - Interprets influence text, artist influences, and usage context
    - Optionally refines the producer plan with LLM intelligence
    - Generates a complete song blueprint with:
      * Enhanced producer plan summary
      * Title and metadata
      * Vocal style
      * Hook and chorus
      * Full song structure with lyrics
      * Procedurally generated audio

    The AI Magic Track provides more sophisticated musical intelligence
    compared to the basic generation endpoint.
    """
    service = MusicService(db)
    result = await service.generate_magic_song(request)
    return result
