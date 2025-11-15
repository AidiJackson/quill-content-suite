"""
Producer Plan Service - Influence & Intent Interpretation.

This module provides a rule-based "producer brain" that interprets user influence text,
artist preferences, and usage context into structured parameters for the procedural music engine.

This is designed to be upgradable to LLM-based interpretation in the future while maintaining
a deterministic, rule-based approach for now.
"""

from typing import Any, Dict, List, Optional
from app.schemas.media import MusicGenerateRequest


class ProducerPlan:
    """
    Structured producer plan that interprets user influences into generation parameters.

    Attributes:
        config: Dictionary of structured parameters for the music engine
        summary: Human-readable summary of how influences were interpreted
    """

    def __init__(self, config: Dict[str, Any], summary: str):
        self.config = config
        self.summary = summary


def build_producer_plan(req: MusicGenerateRequest) -> ProducerPlan:
    """
    Interpret influence_text, influence_artists, usage_context into
    structured parameters for the procedural engine.

    This is a rule-based implementation that provides deterministic behavior.
    Future versions can replace this with LLM-based interpretation.

    Args:
        req: Music generation request with influence fields

    Returns:
        ProducerPlan with structured config and human-readable summary
    """

    # Start with defaults
    tempo_bpm = req.tempo_bpm or 100
    key = "C minor"
    artist_style = req.artist_style or "generic"
    energy_curve = "medium"
    structure = ["intro", "verse", "chorus", "verse", "chorus", "outro"]
    drum_profile = "generic"
    guitar_profile = None
    mood = req.mood or "neutral"

    # Normalize inputs for pattern matching
    text = (req.influence_text or "").lower()
    artists = [a.lower() for a in (req.influence_artists or [])]
    usage = (req.usage_context or "").lower()

    # === TEMPO & ENERGY HEURISTICS ===

    # Slow/ballad indicators
    if any(word in text for word in ["slow", "ballad", "emotional", "intimate"]):
        tempo_bpm = min(tempo_bpm, 90)
        energy_curve = "slow_build"

    # Fast/high energy indicators
    if any(word in text for word in ["fast", "high energy", "aggressive", "intense", "powerful"]):
        tempo_bpm = max(tempo_bpm, 120)
        energy_curve = "high"

    # TikTok/Shorts optimization
    if any(word in text for word in ["tiktok", "shorts", "hook"]) or usage == "tiktok":
        structure = ["intro", "drop", "chorus", "drop"]
        energy_curve = "hook_first"
        tempo_bpm = max(tempo_bpm, 110)  # TikTok tends toward higher energy

    # === HARMONIC MOOD ===

    # Dark/minor key indicators
    if any(word in text for word in ["dark", "emotional", "moody", "sad", "melancholic", "heavy"]):
        key = "D minor"
        mood = "dark"

    # Bright/major key indicators
    if any(word in text for word in ["bright", "uplifting", "hopeful", "happy", "positive"]):
        key = "F major"
        mood = "uplifting"

    # === ARTIST STYLE HEURISTICS ===

    # Linkin Park influence
    if any("linkin park" in a for a in artists) or "linkin park" in text:
        artist_style = "linkin_park"
        guitar_profile = "lp_heavy_guitars"
        drum_profile = "lp_rock_drums"
        if tempo_bpm == 100:  # Override default
            tempo_bpm = 95
        if key == "C minor":
            key = "D minor"

    # Eminem influence
    if any("eminem" in a for a in artists) or "eminem" in text:
        # Hybrid if both Linkin Park and Eminem mentioned
        if artist_style == "linkin_park":
            artist_style = "linkin_park_eminem_hybrid"
        else:
            artist_style = "eminem"
        drum_profile = "eminem_bounce"
        if tempo_bpm == 100:
            tempo_bpm = 92

    # Depeche Mode influence (from existing profiles)
    if any("depeche mode" in a for a in artists) or "depeche mode" in text:
        artist_style = "depeche_mode"
        mood = "dark"
        key = "A minor"

    # Gary Numan influence
    if any("gary numan" in a for a in artists) or "gary numan" in text:
        artist_style = "gary_numan"
        mood = "dystopian"
        key = "G minor"

    # Kraftwerk influence
    if any("kraftwerk" in a for a in artists) or "kraftwerk" in text:
        artist_style = "kraftwerk"
        mood = "mechanical"
        key = "C major"

    # Pet Shop Boys influence
    if any("pet shop boys" in a for a in artists) or "pet shop boys" in text:
        artist_style = "pet_shop_boys"
        mood = "sophisticated"
        key = "D major"

    # === USAGE CONTEXT ADJUSTMENTS ===

    if usage == "background":
        energy_curve = "steady"
        structure = ["loop"]
        tempo_bpm = min(tempo_bpm, 100)  # Background music tends to be more subdued

    if usage == "longform" or usage == "full_song":
        structure = ["intro", "verse", "chorus", "verse", "bridge", "chorus", "outro"]
        energy_curve = "dynamic"

    # === GUITAR/INSTRUMENT DETECTION ===

    if any(word in text for word in ["guitar", "riff", "rock", "metal"]):
        if not guitar_profile:
            guitar_profile = "heavy_guitars"

    if any(word in text for word in ["synth", "electronic", "digital"]):
        guitar_profile = None  # Override guitar if electronic mentioned

    # === BUILD CONFIG ===

    config = {
        "tempo_bpm": tempo_bpm,
        "key": key,
        "artist_style": artist_style,
        "energy_curve": energy_curve,
        "structure": structure,
        "drum_profile": drum_profile,
        "guitar_profile": guitar_profile,
        "mood": mood,
    }

    # === BUILD SUMMARY ===

    summary_parts = []

    # Tempo and key
    summary_parts.append(f"Tempo: {tempo_bpm} BPM in {key}.")

    # Artist influence
    if artist_style != "generic":
        if artist_style == "linkin_park_eminem_hybrid":
            summary_parts.append("Artist influence: Linkin Park + Eminem hybrid.")
        else:
            summary_parts.append(f"Artist influence: {artist_style.replace('_', ' ').title()}.")

    # Usage context
    if usage:
        summary_parts.append(f"Usage: {usage}.")

    # Mood
    if "dark" in text or mood == "dark":
        summary_parts.append("Mood: dark/emotional.")
    elif "uplifting" in text or mood == "uplifting":
        summary_parts.append("Mood: uplifting/positive.")

    # TikTok optimization
    if "tiktok" in text or "shorts" in text or usage == "tiktok":
        summary_parts.append("Optimized for short, hook-first format.")

    # Guitars
    if guitar_profile:
        summary_parts.append("Guitars will be prominent and riff-driven.")

    # Drums
    if drum_profile == "eminem_bounce":
        summary_parts.append("Drums will have a bouncy, hip-hop feel.")
    elif drum_profile == "lp_rock_drums":
        summary_parts.append("Drums will have a heavy rock/metal feel.")

    # Background music
    if usage == "background":
        summary_parts.append("Structured for background/ambient use.")

    summary = " ".join(summary_parts) if summary_parts else "Generic producer plan with default settings."

    return ProducerPlan(config=config, summary=summary)
