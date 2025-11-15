"""Vocal generation service with TTS-based vocal engine."""

import uuid
import os
from typing import Optional
from pathlib import Path

from gtts import gTTS
from app.core.logging import get_logger
from app.schemas.media import VocalGenerateRequest, VocalGenerateResponse

logger = get_logger(__name__)

# Audio storage directory
AUDIO_DIR = Path(__file__).parent.parent.parent / "static" / "audio" / "vocals"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class FakeVocalEngine:
    """
    TTS-based vocal engine for demo purposes.

    Generates real playable audio using Google Text-to-Speech.
    Designed to be swapped with a real singing model later.
    """

    def generate(self, request: VocalGenerateRequest) -> VocalGenerateResponse:
        """
        Generate actual TTS vocal audio from the request.

        Args:
            request: Vocal generation request with lyrics and style

        Returns:
            VocalGenerateResponse with real audio URL and metadata
        """
        # Generate unique vocal ID
        vocal_id = str(uuid.uuid4())

        # Create filename
        filename = f"{vocal_id}.mp3"
        file_path = AUDIO_DIR / filename

        try:
            # Generate TTS audio from lyrics
            # Use slow=False for normal speech speed
            tts = gTTS(text=request.lyrics, lang='en', slow=False)
            tts.save(str(file_path))

            # Get actual file size for duration estimation
            file_size = os.path.getsize(file_path)
            # Rough estimation: ~1 second per 4KB for speech
            duration_seconds = max(10, int(file_size / 4000))

            logger.info(
                f"Generated TTS vocal: {vocal_id} "
                f"({file_size} bytes, ~{duration_seconds}s)"
            )
        except Exception as e:
            logger.error(f"Failed to generate TTS audio: {e}")
            # Fallback to estimation if TTS fails
            duration_seconds = self._estimate_duration(
                lyrics=request.lyrics,
                tempo_bpm=request.tempo_bpm
            )

        # Build audio URL that points to our static file server
        audio_url = f"/static/audio/vocals/{filename}"

        # Add notes
        notes = (
            f"TTS-generated vocals. "
            f"Style: {request.vocal_style.gender} vocals, {request.vocal_style.tone} tone, "
            f"{request.vocal_style.energy} energy. "
            f"Real singing model coming soon."
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
