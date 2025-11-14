"""Music generation routes (STUB)."""

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
    Generate an AI music track (STUB).

    TODO: Replace with real music generation once backend is upgraded.
    """
    service = MusicService(db)

    result = service.generate_track(
        prompt=request.prompt,
        genre=request.genre,
        duration=request.duration or 60,
        project_id=request.project_id,
    )

    return result
