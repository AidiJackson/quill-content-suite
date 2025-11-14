"""Vocal generation routes."""

from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.schemas.media import VocalGenerateRequest, VocalGenerateResponse
from app.services.vocal_service import get_vocal_engine

router = APIRouter(prefix="/vocals", tags=["Vocals"])


@router.post("/generate", response_model=VocalGenerateResponse)
def generate_vocals(
    request: VocalGenerateRequest,
    current_user: CurrentUser,
):
    """
    Generate vocals from lyrics and vocal style.

    Creates a demo vocal rendering with:
    - Unique vocal ID
    - Audio URL (placeholder for now)
    - Estimated duration
    - Vocal style metadata
    - Generation notes

    This is currently using a fake vocal engine for demo purposes.
    In production, this will be replaced with a real singing model.
    """
    engine = get_vocal_engine()
    result = engine.generate(request)
    return result
