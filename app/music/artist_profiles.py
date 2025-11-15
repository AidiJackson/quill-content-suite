"""
Artist-specific musical DNA for procedural music generation.

This module defines musical characteristics (chord progressions, drum grooves,
arpeggiator patterns, scales) for different 80s electronic music artists.
"""

from typing import Dict, List, Any


def get_scale_degrees(scale_name: str) -> List[int]:
    """
    Get semitone offsets for a given scale/mode.

    Args:
        scale_name: Name of scale ("natural_minor", "major", "dorian")

    Returns:
        List of semitone offsets from root
    """
    scales = {
        "natural_minor": [0, 2, 3, 5, 7, 8, 10],  # A minor: A B C D E F G
        "major": [0, 2, 4, 5, 7, 9, 11],           # C major: C D E F G A B
        "dorian": [0, 2, 3, 5, 7, 9, 10],          # D dorian: D E F G A B C
    }
    return scales.get(scale_name, scales["natural_minor"])


def roman_to_semitones(roman: str, scale_name: str) -> List[int]:
    """
    Convert Roman numeral chord notation to semitone offsets.

    Args:
        roman: Roman numeral (e.g., "i", "VI", "III", "VII")
        scale_name: Scale to use for chord construction

    Returns:
        List of 3 semitone offsets representing a triad
    """
    scale = get_scale_degrees(scale_name)

    # Map Roman numerals to scale degrees (0-indexed)
    roman_map = {
        "i": 0, "I": 0,
        "ii": 1, "II": 1,
        "iii": 2, "III": 2,
        "iv": 3, "IV": 3,
        "v": 4, "V": 4,
        "vi": 5, "VI": 5,
        "vii": 6, "VII": 6,
    }

    degree = roman_map.get(roman, 0)

    # Build triad: root, third, fifth (using scale degrees)
    root = scale[degree % len(scale)]
    third = scale[(degree + 2) % len(scale)]
    fifth = scale[(degree + 4) % len(scale)]

    # Handle octave wrapping
    if third < root:
        third += 12
    if fifth < root:
        fifth += 12
    if fifth < third:
        fifth += 12

    return [root, third, fifth]


# Artist-specific musical DNA database
ARTIST_PROFILES: Dict[str, Dict[str, Any]] = {
    "depeche_mode": {
        "scale": "natural_minor",
        "root_midi": 57,  # A3
        "chord_progressions": [
            ["i", "VI", "III", "VII"],   # Dark, melancholic
            ["i", "VII", "VI", "VII"],   # Moody, atmospheric
            ["i", "iv", "VI", "III"],    # Deep, emotional
        ],
        "harmonic_rhythm": "slow",  # 2 bars per chord
        "groove_templates": [
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "hihat_closed": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "hihat_open":   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                "swing_amount": 0.05,
            },
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                "hihat_closed": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "hihat_open":   [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                "swing_amount": 0.08,
            },
        ],
        "arp_patterns": [
            [0, 2, 4, 7, 4, 2],      # Classic arpeggiated minor
            [0, 4, 2, 4, 0, 7],      # Jumping pattern
            [0, 2, 5, 4, 2, 0],      # Descending cascade
        ],
    },

    "gary_numan": {
        "scale": "natural_minor",
        "root_midi": 55,  # G3
        "chord_progressions": [
            ["i", "VII", "i", "VII"],    # Minimalist, robotic
            ["i", "VI", "i", "VI"],      # Cold, mechanical
            ["i", "i", "VII", "VII"],    # Static, dystopian
        ],
        "harmonic_rhythm": "static",  # 4 bars per chord, very static
        "groove_templates": [
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "hihat_closed": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "hihat_open":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "swing_amount": 0.0,  # Rigid, no swing
            },
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "hihat_closed": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "hihat_open":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                "swing_amount": 0.0,
            },
        ],
        "arp_patterns": [
            [0, 0, 0, 0, 2, 2, 2, 2],    # Stuttering, robotic
            [0, 4, 0, 4, 0, 4, 0, 4],    # Machine-like repetition
            [0, 2, 0, 2, 4, 2, 0, 2],    # Sparse, metallic
        ],
    },

    "kraftwerk": {
        "scale": "major",
        "root_midi": 60,  # C4
        "chord_progressions": [
            ["I", "I", "I", "I"],        # Hypnotic minimalism
            ["I", "V", "I", "V"],        # Simple, mechanical
            ["I", "IV", "V", "I"],       # Classic progression
        ],
        "harmonic_rhythm": "rigid",  # 1 bar per chord, very mechanical
        "groove_templates": [
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "hihat_closed": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "hihat_open":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "swing_amount": 0.0,  # Perfect quantization
            },
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                "hihat_closed": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "hihat_open":   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                "swing_amount": 0.0,
            },
        ],
        "arp_patterns": [
            [0, 2, 4, 2],                # Simple, clean
            [0, 4, 7, 4],                # Perfect mechanical
            [0, 0, 4, 4, 7, 7, 4, 4],    # Sequenced, repetitive
        ],
    },

    "pet_shop_boys": {
        "scale": "major",
        "root_midi": 62,  # D4
        "chord_progressions": [
            ["I", "V", "vi", "IV"],      # Pop progression
            ["I", "vi", "IV", "V"],      # Uplifting, melodic
            ["vi", "IV", "I", "V"],      # Emotional, catchy
        ],
        "harmonic_rhythm": "normal",  # 1 bar per chord
        "groove_templates": [
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                "hihat_closed": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "hihat_open":   [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                "swing_amount": 0.1,  # Groovy, syncopated
            },
            {
                "resolution": 16,
                "kick":  [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
                "hihat_closed": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "hihat_open":   [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                "swing_amount": 0.12,
            },
        ],
        "arp_patterns": [
            [0, 2, 4, 7, 9, 7, 4, 2],    # Melodic, poppy
            [0, 4, 7, 4, 9, 7, 4, 0],    # Bright, catchy
            [0, 7, 4, 7, 0, 9, 4, 2],    # Syncopated, danceable
        ],
    },
}


def get_artist_profile(artist_style: str) -> Dict[str, Any]:
    """
    Get the musical profile for a given artist style.

    Args:
        artist_style: Artist style identifier (e.g., "depeche_mode")

    Returns:
        Artist profile dictionary with musical characteristics
    """
    # Default to depeche_mode if not found
    return ARTIST_PROFILES.get(artist_style, ARTIST_PROFILES["depeche_mode"])
