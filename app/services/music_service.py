"""Music generation service with structured song generation."""

import hashlib
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.media_file import MediaFile, MediaType
from app.schemas.media import (MusicGenerateRequest, MusicGenerateResponse,
                                MusicSection, VocalStyle)

logger = get_logger(__name__)


class FakeMusicGenerator:
    """
    Deterministic fake music generator that creates realistic song blueprints.

    This generates structured songs with lyrics, sections, and metadata
    without making any external API calls.
    """

    # Genre-specific templates
    GENRE_TEMPLATES = {
        "trap": {
            "vocal": {"gender": "male", "tone": "aggressive", "energy": "high"},
            "default_bpm": 140,
            "themes": ["money", "hustle", "success", "street life", "ambition"],
        },
        "drill": {
            "vocal": {"gender": "male", "tone": "menacing", "energy": "high"},
            "default_bpm": 145,
            "themes": ["struggle", "survival", "street", "loyalty", "pressure"],
        },
        "afrobeat": {
            "vocal": {"gender": "mixed", "tone": "vibrant", "energy": "high"},
            "default_bpm": 102,
            "themes": ["love", "celebration", "dance", "joy", "culture"],
        },
        "lofi": {
            "vocal": {"gender": "female", "tone": "soft", "energy": "low"},
            "default_bpm": 85,
            "themes": ["reflection", "nostalgia", "peace", "night", "study"],
        },
        "pop": {
            "vocal": {"gender": "female", "tone": "bright", "energy": "medium"},
            "default_bpm": 120,
            "themes": ["love", "heartbreak", "fun", "summer", "dreams"],
        },
        "edm": {
            "vocal": {"gender": "female", "tone": "powerful", "energy": "high"},
            "default_bpm": 128,
            "themes": ["party", "freedom", "energy", "night", "escape"],
        },
        "rnb": {
            "vocal": {"gender": "female", "tone": "smooth", "energy": "medium"},
            "default_bpm": 90,
            "themes": ["love", "emotion", "intimacy", "passion", "soul"],
        },
        "hiphop": {
            "vocal": {"gender": "male", "tone": "confident", "energy": "medium"},
            "default_bpm": 95,
            "themes": ["story", "struggle", "growth", "realness", "legacy"],
        },
    }

    # Mood modifiers
    MOOD_MODIFIERS = {
        "dark": {"tone_mod": "dark", "themes": ["shadows", "mystery", "depth", "intensity"]},
        "energetic": {"tone_mod": "energetic", "themes": ["power", "drive", "motion", "alive"]},
        "emotional": {"tone_mod": "emotional", "themes": ["feelings", "heart", "soul", "vulnerable"]},
        "dreamy": {"tone_mod": "dreamy", "themes": ["clouds", "floating", "ethereal", "imagination"]},
        "uplifting": {"tone_mod": "uplifting", "themes": ["hope", "rise", "light", "positive"]},
        "chill": {"tone_mod": "relaxed", "themes": ["calm", "smooth", "easy", "vibe"]},
    }

    def generate_song(self, request: MusicGenerateRequest) -> MusicGenerateResponse:
        """Generate a complete song blueprint from request."""

        # Get genre template
        genre_lower = request.genre.lower()
        template = self.GENRE_TEMPLATES.get(genre_lower, self.GENRE_TEMPLATES["pop"])

        # Get mood modifier
        mood_lower = request.mood.lower()
        mood_mod = self.MOOD_MODIFIERS.get(mood_lower, self.MOOD_MODIFIERS["energetic"])

        # Generate track ID (deterministic from inputs)
        track_input = f"{request.genre}{request.mood}{request.reference_text or ''}"
        track_id = hashlib.md5(track_input.encode()).hexdigest()[:12]

        # Generate title
        title = self._generate_title(request.genre, request.mood, request.reference_text)

        # Determine tempo
        tempo_bpm = request.tempo_bpm or template["default_bpm"]

        # Create vocal style
        vocal_base = template["vocal"].copy()
        vocal_style = VocalStyle(
            gender=vocal_base["gender"],
            tone=f"{mood_mod['tone_mod']} {vocal_base['tone']}",
            energy=vocal_base["energy"]
        )

        # Generate hook and chorus
        hook = self._generate_hook(request.genre, request.mood, request.reference_text)
        chorus = self._generate_chorus(request.genre, request.mood, request.reference_text, hook)

        # Generate sections
        section_names = request.sections or ["Intro", "Verse 1", "Chorus", "Verse 2", "Bridge", "Chorus", "Outro"]
        sections = self._generate_sections(
            section_names,
            request.genre,
            request.mood,
            request.reference_text,
            chorus
        )

        # Create fake audio URL
        fake_audio_url = f"https://fake-storage.example.com/tracks/{track_id}.mp3"

        return MusicGenerateResponse(
            track_id=track_id,
            title=title,
            genre=request.genre,
            mood=request.mood,
            tempo_bpm=tempo_bpm,
            vocal_style=vocal_style,
            hook=hook,
            chorus=chorus,
            sections=sections,
            fake_audio_url=fake_audio_url,
            saved_media_id=None
        )

    def _generate_title(self, genre: str, mood: str, reference_text: Optional[str]) -> str:
        """Generate a song title."""
        if reference_text and len(reference_text) > 10:
            # Extract keywords from reference
            words = reference_text.split()[:4]
            return " ".join(w.capitalize() for w in words if len(w) > 3)[:40]

        # Generate from genre + mood
        genre_words = {
            "trap": ["Money", "Dreams", "Hustle", "Rise"],
            "drill": ["Pressure", "Streets", "Real", "Survival"],
            "afrobeat": ["Celebration", "Dance", "Joy", "Vibes"],
            "lofi": ["Midnight", "Thoughts", "Coffee", "Rain"],
            "pop": ["Summer", "Dreams", "Heartbeat", "Starlight"],
            "edm": ["Pulse", "Neon", "Eclipse", "Frequency"],
            "rnb": ["Velvet", "Soul", "Emotion", "Intimate"],
            "hiphop": ["Legacy", "Story", "Journey", "Truth"],
        }

        mood_words = {
            "dark": ["Shadows", "Depths", "Mystery"],
            "energetic": ["Energy", "Power", "Drive"],
            "emotional": ["Feelings", "Heart", "Soul"],
            "dreamy": ["Clouds", "Dreams", "Floating"],
            "uplifting": ["Rising", "Light", "Hope"],
            "chill": ["Vibes", "Smooth", "Easy"],
        }

        genre_word = genre_words.get(genre.lower(), ["Song"])[0]
        mood_word = mood_words.get(mood.lower(), ["Vibes"])[0]

        return f"{mood_word} {genre_word}"

    def _generate_hook(self, genre: str, mood: str, reference_text: Optional[str]) -> str:
        """Generate a memorable hook line."""
        templates = [
            f"Can't stop this {mood} feeling",
            f"Living in the {mood} moments",
            f"This is how we {mood.replace('emotional', 'feel')}",
            f"Running through the {mood} nights",
            f"We're rising from the {mood} depths",
        ]

        # Use hash to deterministically pick a template
        idx = hash(f"{genre}{mood}") % len(templates)
        return templates[idx]

    def _generate_chorus(self, genre: str, mood: str, reference_text: Optional[str], hook: str) -> str:
        """Generate main chorus lyrics."""
        return f"""{hook}
Never looking back, we're moving forward now
Every single moment, yeah we're living loud
{hook}
This is our time, this is our sound"""

    def _generate_sections(
        self,
        section_names: List[str],
        genre: str,
        mood: str,
        reference_text: Optional[str],
        chorus: str
    ) -> List[MusicSection]:
        """Generate all song sections with lyrics."""
        sections = []

        for section_name in section_names:
            section_lower = section_name.lower()

            if "intro" in section_lower:
                sections.append(MusicSection(
                    name=section_name,
                    bars=8,
                    description="Atmospheric intro with melodic elements",
                    lyrics="[Instrumental with ambient sounds]"
                ))

            elif "verse" in section_lower:
                verse_num = "1" if "verse 1" in section_lower or section_lower == "verse" else "2"
                sections.append(MusicSection(
                    name=section_name,
                    bars=16,
                    description=f"Story development, building energy",
                    lyrics=self._generate_verse_lyrics(genre, mood, verse_num)
                ))

            elif "chorus" in section_lower:
                sections.append(MusicSection(
                    name=section_name,
                    bars=16,
                    description="Main hook section, maximum energy",
                    lyrics=chorus
                ))

            elif "bridge" in section_lower:
                sections.append(MusicSection(
                    name=section_name,
                    bars=8,
                    description="Musical break, change in dynamics",
                    lyrics=self._generate_bridge_lyrics(genre, mood)
                ))

            elif "outro" in section_lower:
                sections.append(MusicSection(
                    name=section_name,
                    bars=8,
                    description="Gradual fade with repeated hook elements",
                    lyrics="[Instrumental fade with vocal echoes]"
                ))

            else:
                # Generic section
                sections.append(MusicSection(
                    name=section_name,
                    bars=12,
                    description="Musical section",
                    lyrics=self._generate_verse_lyrics(genre, mood, "1")
                ))

        return sections

    def _generate_verse_lyrics(self, genre: str, mood: str, verse_num: str) -> str:
        """Generate verse lyrics."""
        verse_templates = {
            "1": """Started from the bottom, now we're on the rise
Every single struggle turned to fire in our eyes
No more looking backwards, only forward from here
Living in the moment, letting go of the fear""",
            "2": """They said we couldn't make it, said we'd never survive
But we proved them all wrong, now we're feeling alive
Every obstacle we faced just made us more strong
This is our story, this is our song"""
        }

        return verse_templates.get(verse_num, verse_templates["1"])

    def _generate_bridge_lyrics(self, genre: str, mood: str) -> str:
        """Generate bridge lyrics."""
        return """And when the lights go down
We'll still be standing proud
Nothing can stop us now
We're breaking through the clouds"""


class MusicService:
    """Service for music generation operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize music service."""
        self.db = db
        self.generator = FakeMusicGenerator()

    def generate_song(self, request: MusicGenerateRequest) -> MusicGenerateResponse:
        """
        Generate a complete song blueprint.

        Creates structured output with lyrics, sections, and metadata.
        """
        logger.info(f"Generating song: genre={request.genre}, mood={request.mood}")

        # Generate the song
        response = self.generator.generate_song(request)

        # Save to database if project_id provided
        if request.project_id and self.db:
            saved_media_id = self._save_media_file(
                project_id=request.project_id,
                url=response.fake_audio_url,
                metadata={
                    "track_id": response.track_id,
                    "title": response.title,
                    "genre": response.genre,
                    "mood": response.mood,
                    "tempo_bpm": response.tempo_bpm,
                    "operation": "song_generation",
                }
            )
            response.saved_media_id = saved_media_id

        logger.info(f"Generated song: {response.title} ({response.track_id})")
        return response

    def _save_media_file(
        self,
        project_id: str,
        url: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Save media file to database."""
        if not self.db:
            raise ValueError("Database session required to save media")

        media = MediaFile(
            project_id=project_id,
            url=url,
            type=MediaType.AUDIO,
            meta=metadata,
        )

        self.db.add(media)
        self.db.commit()
        self.db.refresh(media)

        logger.info(f"Saved media file: {media.id}")
        return media.id
