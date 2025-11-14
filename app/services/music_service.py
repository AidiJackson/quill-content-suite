"""Music generation service (MVP stub implementation)."""

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.media_file import MediaFile, MediaType

logger = get_logger(__name__)


class MusicService:
    """Service for music generation operations (MVP stubs)."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize music service."""
        self.db = db

    def generate_track(
        self,
        prompt: Optional[str] = None,
        genre: Optional[str] = None,
        duration: int = 60,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a music track (STUB implementation for MVP).

        TODO: Replace with real AI music generation once backend is upgraded.
        """
        prompt_str = prompt or "ambient music"
        genre_str = genre or "electronic"
        logger.info(f"Generating music track: {prompt_str}, genre: {genre_str}")

        # Fake output URL
        track_id = hash(f"{prompt_str}{genre_str}") % 10000
        output_url = f"https://fake-storage.example.com/music_track_{track_id}.mp3"

        metadata = {
            "operation": "music_generation",
            "prompt": prompt_str,
            "genre": genre_str,
            "duration": duration,
            "generator": "stub",
            "format": "mp3",
        }

        saved_media_id = None
        if project_id and self.db:
            saved_media_id = self._save_media_file(
                project_id=project_id,
                url=output_url,
                media_type=MediaType.AUDIO,
                metadata=metadata,
            )

        return {
            "track_url": output_url,
            "duration": duration,
            "metadata": metadata,
            "saved_media_id": saved_media_id,
        }

    def _save_media_file(
        self,
        project_id: str,
        url: str,
        media_type: MediaType,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Save media file to database."""
        if not self.db:
            raise ValueError("Database session required to save media")

        media = MediaFile(
            project_id=project_id,
            url=url,
            type=media_type,
            meta=metadata,
        )

        self.db.add(media)
        self.db.commit()
        self.db.refresh(media)

        logger.info(f"Saved media file: {media.id}")
        return media.id
