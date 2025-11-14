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
