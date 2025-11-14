"""Vocal generation service with fake/demo vocal engine."""

import uuid
from typing import Optional

from app.core.logging import get_logger
from app.schemas.media import VocalGenerateRequest, VocalGenerateResponse

logger = get_logger(__name__)


class FakeVocalEngine:
    """
    Deterministic fake vocal engine for demo purposes.

    This generates realistic-looking vocal outputs without actually
    rendering audio. Designed to be swapped with a real singing model later.
    """

    def generate(self, request: VocalGenerateRequest) -> VocalGenerateResponse:
        """
        Generate a fake vocal rendering from the request.

        Args:
            request: Vocal generation request with lyrics and style

        Returns:
            VocalGenerateResponse with demo audio URL and metadata
        """
        # Generate unique vocal ID
        vocal_id = str(uuid.uuid4())

        # Build deterministic audio URL
        gender = request.vocal_style.gender.lower()
        energy = request.vocal_style.energy.lower()
        audio_url = f"https://demo.quillography.ai/audio/vocals/{gender}-{energy}-{vocal_id}.mp3"

        # Estimate duration based on lyrics and tempo
        duration_seconds = self._estimate_duration(
            lyrics=request.lyrics,
            tempo_bpm=request.tempo_bpm
        )

        # Add demo notes
        notes = (
            f"Demo vocal rendering (fake engine). "
            f"Style: {request.vocal_style.gender} vocals, {request.vocal_style.tone} tone, "
            f"{request.vocal_style.energy} energy. "
            f"Replace with real singing model output."
        )

        logger.info(
            f"Generated fake vocal: {vocal_id} "
            f"({gender}/{energy}, ~{duration_seconds}s)"
        )

        return VocalGenerateResponse(
            vocal_id=vocal_id,
            track_id=request.track_id,
            audio_url=audio_url,
            duration_seconds=duration_seconds,
            vocal_style=request.vocal_style,
            notes=notes
        )

    def _estimate_duration(
        self,
        lyrics: str,
        tempo_bpm: Optional[int] = None
    ) -> int:
        """
        Estimate song duration from lyrics and tempo.

        Args:
            lyrics: Song lyrics text
            tempo_bpm: Tempo in beats per minute

        Returns:
            Estimated duration in seconds
        """
        # Count words as a proxy for length
        word_count = len(lyrics.split())

        # Use tempo to adjust (faster tempo = more words per second)
        tempo = tempo_bpm or 120
        words_per_second = tempo / 120 * 2.5  # Rough approximation

        # Calculate duration
        duration = int(word_count / words_per_second)

        # Clamp between 30 and 240 seconds
        duration = max(30, min(240, duration))

        return duration


def get_vocal_engine() -> FakeVocalEngine:
    """
    Get the vocal engine instance.

    Returns singleton FakeVocalEngine for now.
    Later, this can be swapped to return RealVocalEngine
    based on configuration.
    """
    return FakeVocalEngine()
