"""Music generation service with structured song generation."""

import hashlib
import uuid
from typing import Any, Dict, List, Optional
from pathlib import Path

import numpy as np
import soundfile as sf
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.media_file import MediaFile, MediaType
from app.schemas.media import (MusicGenerateRequest, MusicGenerateResponse,
                                MusicSection, VocalStyle)

logger = get_logger(__name__)

# Audio storage directory
AUDIO_DIR = Path(__file__).parent.parent.parent / "static" / "audio" / "music"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class ProceduralMusicEngine:
    """
    Procedural music composition engine.

    Generates simple instrumental backing tracks using NumPy,
    with genre-specific drums, bass, and optional pads.
    """

    SAMPLE_RATE = 44100

    # Genre-specific musical parameters
    GENRE_PARAMS = {
        "trap": {
            "scale": [55, 65.4, 73.4, 82.4, 98, 110],  # A minor pentatonic (bass)
            "kick_pattern": [1, 0, 0, 0, 1, 0, 1, 0],  # More kicks for trap
            "snare_pattern": [0, 0, 1, 0, 0, 0, 1, 0],
            "hihat_pattern": [1, 1, 1, 1, 1, 1, 1, 1],  # Constant hats
            "bass_intensity": 0.4,
        },
        "drill": {
            "scale": [49, 58.3, 65.4, 73.4, 87.3, 98],  # G minor pentatonic
            "kick_pattern": [1, 0, 1, 0, 1, 0, 0, 0],
            "snare_pattern": [0, 0, 1, 0, 0, 0, 1, 0],
            "hihat_pattern": [1, 1, 1, 1, 1, 1, 1, 1],
            "bass_intensity": 0.5,
        },
        "pop": {
            "scale": [65.4, 73.4, 82.4, 87.3, 98, 110],  # C major
            "kick_pattern": [1, 0, 0, 0, 1, 0, 0, 0],
            "snare_pattern": [0, 0, 1, 0, 0, 0, 1, 0],
            "hihat_pattern": [0, 1, 0, 1, 0, 1, 0, 1],
            "bass_intensity": 0.3,
        },
        "lofi": {
            "scale": [55, 61.7, 69.3, 82.4, 92.5, 110],  # A minor (jazzy)
            "kick_pattern": [1, 0, 0, 0, 0, 0, 1, 0],
            "snare_pattern": [0, 0, 0, 1, 0, 0, 0, 1],
            "hihat_pattern": [0, 0, 1, 0, 0, 0, 1, 0],  # Sparse
            "bass_intensity": 0.25,
        },
        "edm": {
            "scale": [49, 58.3, 65.4, 77.8, 87.3, 98],  # G major
            "kick_pattern": [1, 0, 0, 0, 1, 0, 0, 0],
            "snare_pattern": [0, 0, 1, 0, 0, 0, 1, 0],
            "hihat_pattern": [1, 1, 1, 1, 1, 1, 1, 1],
            "bass_intensity": 0.4,
        },
        "rnb": {
            "scale": [58.3, 65.4, 73.4, 77.8, 87.3, 98],  # Bb major
            "kick_pattern": [1, 0, 0, 0, 0, 1, 0, 0],
            "snare_pattern": [0, 0, 1, 0, 0, 0, 1, 0],
            "hihat_pattern": [0, 1, 0, 1, 0, 1, 0, 1],
            "bass_intensity": 0.3,
        },
        "hiphop": {
            "scale": [55, 65.4, 73.4, 82.4, 98, 110],  # A minor
            "kick_pattern": [1, 0, 0, 0, 1, 0, 0, 0],
            "snare_pattern": [0, 0, 1, 0, 0, 0, 1, 0],
            "hihat_pattern": [0, 1, 0, 1, 0, 1, 0, 1],
            "bass_intensity": 0.35,
        },
        "afrobeat": {
            "scale": [65.4, 73.4, 82.4, 98, 110, 130.8],  # C major
            "kick_pattern": [1, 0, 1, 0, 1, 0, 0, 1],
            "snare_pattern": [0, 0, 1, 0, 0, 1, 0, 0],
            "hihat_pattern": [1, 1, 1, 1, 1, 1, 1, 1],
            "bass_intensity": 0.35,
        },
    }

    def generate_backing_track(self, request: MusicGenerateRequest) -> str:
        """
        Generate a procedural backing track based on genre, mood, and tempo.

        Args:
            request: Music generation request with genre, mood, tempo_bpm

        Returns:
            URL path to the generated audio file
        """
        try:
            # Get parameters
            genre = request.genre.lower()
            tempo_bpm = request.tempo_bpm or 120

            # Calculate timing
            bars = 8
            beats_per_bar = 4
            duration_seconds = bars * beats_per_bar * 60 / tempo_bpm
            num_samples = int(duration_seconds * self.SAMPLE_RATE)

            # Get genre parameters (default to pop if not found)
            params = self.GENRE_PARAMS.get(genre, self.GENRE_PARAMS["pop"])

            # Generate track components
            kick = self._generate_kick(num_samples, tempo_bpm, params["kick_pattern"])
            snare = self._generate_snare(num_samples, tempo_bpm, params["snare_pattern"])
            hihat = self._generate_hihat(num_samples, tempo_bpm, params["hihat_pattern"])
            bass = self._generate_bass(num_samples, tempo_bpm, params["scale"], params["bass_intensity"])

            # Add pad for uplifting/dreamy moods
            if request.mood.lower() in ["uplifting", "dreamy", "emotional"]:
                pad = self._generate_pad(num_samples, tempo_bpm, params["scale"])
                mix = kick + snare + hihat + bass + pad
            else:
                mix = kick + snare + hihat + bass

            # Normalize to prevent clipping
            max_val = np.max(np.abs(mix))
            if max_val > 0:
                mix = mix / max_val * 0.85  # Leave headroom

            # Apply fade in/out
            fade_samples = int(0.5 * self.SAMPLE_RATE)  # 0.5 second fade
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            mix[:fade_samples] *= fade_in
            mix[-fade_samples:] *= fade_out

            # Generate track ID
            track_input = f"{request.genre}{request.mood}{request.reference_text or ''}"
            track_id = hashlib.md5(track_input.encode()).hexdigest()[:12]

            # Save to file
            filename = f"track-{track_id}.wav"
            file_path = AUDIO_DIR / filename
            sf.write(str(file_path), mix, self.SAMPLE_RATE)

            logger.info(f"Generated procedural track: {track_id} ({genre}, {tempo_bpm} BPM, {duration_seconds:.1f}s)")

            return f"/static/audio/music/{filename}"

        except Exception as e:
            logger.error(f"Failed to generate procedural music: {e}")
            return f"/static/audio/music/placeholder.wav"

    def _generate_kick(self, num_samples: int, tempo_bpm: float, pattern: List[int]) -> np.ndarray:
        """Generate kick drum track."""
        track = np.zeros(num_samples)
        samples_per_beat = int(60 * self.SAMPLE_RATE / tempo_bpm)

        beat_index = 0
        current_sample = 0

        while current_sample < num_samples:
            if pattern[beat_index % len(pattern)] == 1:
                # Create kick: low frequency sine with exponential decay
                kick_duration = int(0.15 * self.SAMPLE_RATE)
                t = np.arange(kick_duration) / self.SAMPLE_RATE
                freq = 60  # Low frequency
                envelope = np.exp(-10 * t)  # Fast decay
                kick = 0.8 * np.sin(2 * np.pi * freq * t * (1 - 0.7 * t)) * envelope

                end_sample = min(current_sample + kick_duration, num_samples)
                actual_duration = end_sample - current_sample
                track[current_sample:end_sample] += kick[:actual_duration]

            current_sample += samples_per_beat
            beat_index += 1

        return track

    def _generate_snare(self, num_samples: int, tempo_bpm: float, pattern: List[int]) -> np.ndarray:
        """Generate snare drum track."""
        track = np.zeros(num_samples)
        samples_per_beat = int(60 * self.SAMPLE_RATE / tempo_bpm)

        beat_index = 0
        current_sample = 0

        while current_sample < num_samples:
            if pattern[beat_index % len(pattern)] == 1:
                # Create snare: noise burst with envelope
                snare_duration = int(0.1 * self.SAMPLE_RATE)
                t = np.arange(snare_duration) / self.SAMPLE_RATE
                noise = np.random.randn(snare_duration)
                envelope = np.exp(-20 * t)
                snare = 0.3 * noise * envelope

                end_sample = min(current_sample + snare_duration, num_samples)
                actual_duration = end_sample - current_sample
                track[current_sample:end_sample] += snare[:actual_duration]

            current_sample += samples_per_beat
            beat_index += 1

        return track

    def _generate_hihat(self, num_samples: int, tempo_bpm: float, pattern: List[int]) -> np.ndarray:
        """Generate hi-hat track."""
        track = np.zeros(num_samples)
        samples_per_beat = int(60 * self.SAMPLE_RATE / tempo_bpm)

        beat_index = 0
        current_sample = 0

        while current_sample < num_samples:
            if pattern[beat_index % len(pattern)] == 1:
                # Create hi-hat: high-frequency noise burst
                hihat_duration = int(0.05 * self.SAMPLE_RATE)
                noise = np.random.randn(hihat_duration)
                # High-pass filter (simple)
                hihat = np.diff(noise, prepend=0)
                envelope = np.exp(-50 * np.arange(hihat_duration) / self.SAMPLE_RATE)
                hihat = 0.15 * hihat * envelope

                end_sample = min(current_sample + hihat_duration, num_samples)
                actual_duration = end_sample - current_sample
                track[current_sample:end_sample] += hihat[:actual_duration]

            current_sample += samples_per_beat
            beat_index += 1

        return track

    def _generate_bass(self, num_samples: int, tempo_bpm: float, scale: List[float], intensity: float) -> np.ndarray:
        """Generate bassline track."""
        track = np.zeros(num_samples)
        samples_per_bar = int(4 * 60 * self.SAMPLE_RATE / tempo_bpm)

        # Simple progression: I - VI - VII - V (in terms of scale degrees)
        progression = [scale[0], scale[4], scale[5], scale[3]]

        bar_index = 0
        current_sample = 0

        while current_sample < num_samples:
            freq = progression[bar_index % len(progression)]
            bar_duration = min(samples_per_bar, num_samples - current_sample)
            t = np.arange(bar_duration) / self.SAMPLE_RATE

            # Bass note with slight envelope
            bass_note = intensity * np.sin(2 * np.pi * freq * t)
            # Add subtle envelope
            envelope = 1 - 0.3 * t / (bar_duration / self.SAMPLE_RATE)
            envelope = np.clip(envelope, 0, 1)

            track[current_sample:current_sample + bar_duration] = bass_note * envelope

            current_sample += samples_per_bar
            bar_index += 1

        return track

    def _generate_pad(self, num_samples: int, tempo_bpm: float, scale: List[float]) -> np.ndarray:
        """Generate sustained pad/chord track."""
        track = np.zeros(num_samples)
        samples_per_2bars = int(8 * 60 * self.SAMPLE_RATE / tempo_bpm)

        # Simple chord progression using scale notes
        chords = [
            [scale[0], scale[2], scale[4]],  # Root triad
            [scale[3], scale[5], scale[1]],  # Different voicing
        ]

        chord_index = 0
        current_sample = 0

        while current_sample < num_samples:
            chord = chords[chord_index % len(chords)]
            chord_duration = min(samples_per_2bars, num_samples - current_sample)
            t = np.arange(chord_duration) / self.SAMPLE_RATE

            # Generate chord by summing frequencies
            chord_sound = np.zeros(chord_duration)
            for freq in chord:
                chord_sound += 0.05 * np.sin(2 * np.pi * freq * t)

            # Add vibrato for interest
            vibrato = 0.002 * np.sin(2 * np.pi * 5 * t)  # 5 Hz vibrato
            for i, freq in enumerate(chord):
                chord_sound += 0.05 * np.sin(2 * np.pi * freq * t * (1 + vibrato))

            track[current_sample:current_sample + chord_duration] = chord_sound

            current_sample += samples_per_2bars
            chord_index += 1

        return track


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

        # Generate actual audio file
        audio_url = self._generate_audio(request)

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
            fake_audio_url=audio_url,
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

    def _generate_audio(self, request: MusicGenerateRequest) -> str:
        """
        Generate a procedural backing track using the ProceduralMusicEngine.

        Args:
            request: Full music generation request with genre, mood, tempo

        Returns:
            URL path to the generated audio file
        """
        engine = ProceduralMusicEngine()
        return engine.generate_backing_track(request)


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
