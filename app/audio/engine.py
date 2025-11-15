"""
Advanced Synth Engine v1 - Multi-layer procedural audio generation.

This module provides a section-based synthesis engine that generates 40-60 second
backing tracks using numpy and soundfile. It uses the ProducerPlan to drive
tempo, key, structure, artist style, and energy curves.
"""

import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path

from app.core.logging import get_logger
from app.services.producer_plan_service import ProducerPlan

logger = get_logger(__name__)

# ==================== AUDIO CONSTANTS ====================

SAMPLE_RATE = 44100  # 44.1kHz standard audio
BIT_DEPTH = 16  # 16-bit PCM

# ==================== BASIC WAVEFORM GENERATORS ====================


def sine(freq: float, duration: float, volume: float = 1.0) -> np.ndarray:
    """Generate a sine wave.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        volume: Amplitude (0.0 to 1.0)

    Returns:
        Mono audio array
    """
    samples = int(duration * SAMPLE_RATE)
    t = np.arange(samples) / SAMPLE_RATE
    return volume * np.sin(2 * np.pi * freq * t)


def saw(freq: float, duration: float, volume: float = 1.0) -> np.ndarray:
    """Generate a sawtooth wave.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        volume: Amplitude (0.0 to 1.0)

    Returns:
        Mono audio array
    """
    samples = int(duration * SAMPLE_RATE)
    t = np.arange(samples) / SAMPLE_RATE
    return volume * (2 * (t * freq % 1) - 1)


def square(freq: float, duration: float, volume: float = 1.0, duty_cycle: float = 0.5) -> np.ndarray:
    """Generate a square/pulse wave.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        volume: Amplitude (0.0 to 1.0)
        duty_cycle: Pulse width (0.0 to 1.0)

    Returns:
        Mono audio array
    """
    samples = int(duration * SAMPLE_RATE)
    t = np.arange(samples) / SAMPLE_RATE
    return volume * np.where((t * freq % 1) < duty_cycle, 1, -1)


# ==================== ADSR ENVELOPE ====================


def adsr(attack: float, decay: float, sustain_level: float, release: float,
         total_length_samples: int) -> np.ndarray:
    """Generate an ADSR envelope.

    Args:
        attack: Attack time in seconds
        decay: Decay time in seconds
        sustain_level: Sustain level (0.0 to 1.0)
        release: Release time in seconds
        total_length_samples: Total length in samples

    Returns:
        Envelope array
    """
    attack_samples = int(attack * SAMPLE_RATE)
    decay_samples = int(decay * SAMPLE_RATE)
    release_samples = int(release * SAMPLE_RATE)

    envelope = np.zeros(total_length_samples)

    # Attack
    if attack_samples > 0 and attack_samples <= total_length_samples:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        current_pos = attack_samples
    else:
        current_pos = 0

    # Decay
    if current_pos + decay_samples <= total_length_samples:
        envelope[current_pos:current_pos + decay_samples] = np.linspace(1, sustain_level, decay_samples)
        current_pos += decay_samples

    # Sustain
    if current_pos + release_samples <= total_length_samples:
        envelope[current_pos:-release_samples] = sustain_level
        # Release
        envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)
    elif current_pos < total_length_samples:
        # No room for full release, just fade out what's left
        remaining = total_length_samples - current_pos
        envelope[current_pos:] = np.linspace(sustain_level, 0, remaining)

    return envelope


# ==================== SIMPLE FILTERS ====================


def lowpass_filter(signal: np.ndarray, cutoff: float = 0.5) -> np.ndarray:
    """Apply a simple low-pass filter using exponential smoothing.

    Args:
        signal: Input audio signal
        cutoff: Filter cutoff (0.0 to 1.0, lower = more filtering)

    Returns:
        Filtered signal
    """
    filtered = np.zeros_like(signal)
    filtered[0] = signal[0]
    for i in range(1, len(signal)):
        filtered[i] = cutoff * signal[i] + (1 - cutoff) * filtered[i - 1]
    return filtered


def highpass_filter(signal: np.ndarray, cutoff: float = 0.1) -> np.ndarray:
    """Apply a simple high-pass filter using differentiation.

    Args:
        signal: Input audio signal
        cutoff: Filter strength (0.0 to 1.0)

    Returns:
        Filtered signal
    """
    # Simple high-pass: signal - lowpass
    low = lowpass_filter(signal, cutoff)
    return signal - low * 0.8


# ==================== INSTRUMENT GENERATORS ====================


def generate_kick(pattern: List[int], tempo_bpm: float, length_seconds: float,
                  style: str = "808") -> np.ndarray:
    """Generate kick drum pattern.

    Args:
        pattern: List of 0s and 1s indicating when kicks hit
        tempo_bpm: Tempo in beats per minute
        length_seconds: Total length in seconds
        style: Drum machine style ("808", "909", "acoustic")

    Returns:
        Mono kick track
    """
    num_samples = int(length_seconds * SAMPLE_RATE)
    track = np.zeros(num_samples)
    samples_per_beat = int(60 * SAMPLE_RATE / tempo_bpm)

    beat_index = 0
    current_sample = 0

    while current_sample < num_samples:
        if pattern[beat_index % len(pattern)] == 1:
            # Generate kick based on style
            if style == "808":
                kick = _generate_808_kick()
            elif style == "909":
                kick = _generate_909_kick()
            else:  # acoustic
                kick = _generate_acoustic_kick()

            end_sample = min(current_sample + len(kick), num_samples)
            actual_duration = end_sample - current_sample
            track[current_sample:end_sample] += kick[:actual_duration]

        current_sample += samples_per_beat
        beat_index += 1

    return track


def _generate_808_kick() -> np.ndarray:
    """Generate TR-808 style kick - deep, boomy."""
    duration = int(0.4 * SAMPLE_RATE)
    t = np.arange(duration) / SAMPLE_RATE

    # Pitch envelope
    freq_start, freq_end = 180, 35
    freq_env = freq_start * np.exp(-6 * t) + freq_end

    # Amplitude envelope
    amp_env = np.exp(-4.5 * t)

    # Sine oscillator with pitch envelope
    phase = 2 * np.pi * np.cumsum(freq_env) / SAMPLE_RATE
    kick = 1.0 * np.sin(phase) * amp_env

    # Add sub-harmonic
    sub_freq_env = freq_env * 0.5
    sub_phase = 2 * np.pi * np.cumsum(sub_freq_env) / SAMPLE_RATE
    kick += 0.3 * np.sin(sub_phase) * amp_env

    # Attack click
    click_duration = int(0.002 * SAMPLE_RATE)
    click = np.zeros(duration)
    click[:click_duration] = np.exp(-500 * t[:click_duration]) * 0.15

    # Noise texture
    noise = np.random.randn(duration) * np.exp(-50 * t) * 0.05

    return kick + click + noise


def _generate_909_kick() -> np.ndarray:
    """Generate TR-909 style kick - punchy, tight."""
    duration = int(0.18 * SAMPLE_RATE)
    t = np.arange(duration) / SAMPLE_RATE

    # Sharp pitch envelope
    freq_start, freq_end = 220, 55
    freq_env = freq_start * np.exp(-12 * t) + freq_end

    # Tight amplitude envelope
    amp_env = np.exp(-10 * t)

    # Sine with distortion
    phase = 2 * np.pi * np.cumsum(freq_env) / SAMPLE_RATE
    kick = 0.95 * np.sin(phase) * amp_env
    kick += 0.15 * np.sin(2 * phase) * amp_env * np.exp(-15 * t)

    # Pronounced click
    click_duration = int(0.003 * SAMPLE_RATE)
    click = np.zeros(duration)
    click_env = np.exp(-600 * t[:click_duration])
    click[:click_duration] = np.random.randn(click_duration) * click_env * 0.25

    return kick + click


def _generate_acoustic_kick() -> np.ndarray:
    """Generate acoustic-style kick - natural."""
    duration = int(0.22 * SAMPLE_RATE)
    t = np.arange(duration) / SAMPLE_RATE

    # Moderate pitch envelope
    freq_start, freq_end = 140, 50
    freq_env = freq_start * np.exp(-7 * t) + freq_end

    # Natural decay
    amp_env = np.exp(-6 * t)

    # Sine with harmonics
    phase = 2 * np.pi * np.cumsum(freq_env) / SAMPLE_RATE
    kick = 0.85 * np.sin(phase) * amp_env
    kick += 0.1 * np.sin(1.5 * phase) * amp_env

    # Soft attack
    attack_duration = int(0.005 * SAMPLE_RATE)
    attack = np.ones(duration)
    attack[:attack_duration] = np.linspace(0, 1, attack_duration) ** 0.5
    kick = kick * attack

    # Texture noise
    noise = np.random.randn(duration) * np.exp(-30 * t) * 0.08

    return kick + noise


def generate_snare(pattern: List[int], tempo_bpm: float, length_seconds: float,
                   style: str = "808") -> np.ndarray:
    """Generate snare drum pattern.

    Args:
        pattern: List of 0s and 1s indicating when snares hit
        tempo_bpm: Tempo in beats per minute
        length_seconds: Total length in seconds
        style: Drum machine style

    Returns:
        Mono snare track
    """
    num_samples = int(length_seconds * SAMPLE_RATE)
    track = np.zeros(num_samples)
    samples_per_beat = int(60 * SAMPLE_RATE / tempo_bpm)

    beat_index = 0
    current_sample = 0

    while current_sample < num_samples:
        if pattern[beat_index % len(pattern)] == 1:
            if style == "808":
                snare = _generate_808_snare()
            elif style == "909":
                snare = _generate_909_snare()
            else:
                snare = _generate_acoustic_snare()

            end_sample = min(current_sample + len(snare), num_samples)
            actual_duration = end_sample - current_sample
            track[current_sample:end_sample] += snare[:actual_duration]

        current_sample += samples_per_beat
        beat_index += 1

    return track


def _generate_808_snare() -> np.ndarray:
    """TR-808 snare - metallic, filtered noise."""
    duration = int(0.15 * SAMPLE_RATE)
    t = np.arange(duration) / SAMPLE_RATE

    # Tonal components
    tone1 = np.sin(2 * np.pi * 180 * t)
    tone2 = np.sin(2 * np.pi * 330 * t)

    # White noise
    noise = np.random.randn(duration)

    # Envelope
    envelope = np.exp(-25 * t)

    return 0.4 * (0.6 * (tone1 + tone2) + 0.4 * noise) * envelope


def _generate_909_snare() -> np.ndarray:
    """TR-909 snare - crisp, bright."""
    duration = int(0.12 * SAMPLE_RATE)
    t = np.arange(duration) / SAMPLE_RATE

    tone = np.sin(2 * np.pi * 200 * t)
    noise = np.random.randn(duration)
    envelope = np.exp(-30 * t)

    return 0.45 * (0.3 * tone + 0.7 * noise) * envelope


def _generate_acoustic_snare() -> np.ndarray:
    """Acoustic snare - natural."""
    duration = int(0.18 * SAMPLE_RATE)
    t = np.arange(duration) / SAMPLE_RATE

    noise = np.random.randn(duration)
    tone = np.sin(2 * np.pi * 220 * t)
    envelope = np.exp(-15 * t)

    return 0.4 * (0.25 * tone + 0.75 * noise) * envelope


def generate_hihat(pattern: List[int], tempo_bpm: float, length_seconds: float) -> np.ndarray:
    """Generate hi-hat pattern.

    Args:
        pattern: List of 0s and 1s indicating when hihats hit
        tempo_bpm: Tempo in beats per minute
        length_seconds: Total length in seconds

    Returns:
        Mono hihat track
    """
    num_samples = int(length_seconds * SAMPLE_RATE)
    track = np.zeros(num_samples)
    samples_per_beat = int(60 * SAMPLE_RATE / tempo_bpm)

    beat_index = 0
    current_sample = 0

    while current_sample < num_samples:
        if pattern[beat_index % len(pattern)] == 1:
            # Generate hihat
            hihat_duration = int(0.06 * SAMPLE_RATE)
            noise = np.random.randn(hihat_duration)
            hihat = highpass_filter(noise, 0.3)
            envelope = np.exp(-60 * np.arange(hihat_duration) / SAMPLE_RATE)
            hihat = 0.18 * hihat * envelope

            end_sample = min(current_sample + hihat_duration, num_samples)
            actual_duration = end_sample - current_sample
            track[current_sample:end_sample] += hihat[:actual_duration]

        current_sample += samples_per_beat
        beat_index += 1

    return track


def generate_bassline(chord_progression: List[float], tempo_bpm: float, key: str,
                      length_seconds: float, style: str = "synth") -> np.ndarray:
    """Generate bassline.

    Args:
        chord_progression: List of root frequencies
        tempo_bpm: Tempo in beats per minute
        key: Musical key (e.g., "C minor")
        length_seconds: Total length in seconds
        style: Bass style ("synth", "moog", "sequenced", "driving")

    Returns:
        Mono bass track
    """
    num_samples = int(length_seconds * SAMPLE_RATE)
    track = np.zeros(num_samples)
    samples_per_bar = int(4 * 60 * SAMPLE_RATE / tempo_bpm)

    bar_index = 0
    current_sample = 0

    while current_sample < num_samples:
        freq = chord_progression[bar_index % len(chord_progression)]
        bar_duration = min(samples_per_bar, num_samples - current_sample)
        t = np.arange(bar_duration) / SAMPLE_RATE

        if style == "moog":
            # Fat detuned sawtooth
            saw1 = saw(freq * 0.998, bar_duration / SAMPLE_RATE, volume=0.33)
            saw2 = saw(freq, bar_duration / SAMPLE_RATE, volume=0.33)
            saw3 = saw(freq * 1.002, bar_duration / SAMPLE_RATE, volume=0.33)
            sawtooth = saw1 + saw2 + saw3

            # Filter envelope
            filter_env = 0.3 + 0.4 * np.exp(-0.5 * t)
            filtered = sawtooth * filter_env

            # Sub bass
            sub = sine(freq * 0.5, bar_duration / SAMPLE_RATE, volume=0.3)

            # ADSR
            env = adsr(0.005, 0.15, 0.65, 0.25, bar_duration)
            bass_note = 0.4 * (filtered * 0.7 + sub * 0.3) * env

        elif style == "sequenced":
            # Plucky square wave
            pulse = square(freq, bar_duration / SAMPLE_RATE, volume=0.6, duty_cycle=0.25)
            env = np.exp(-20 * t)
            bass_note = 0.35 * pulse * env

        elif style == "driving":
            # Sine with envelope
            bass_sine = sine(freq, bar_duration / SAMPLE_RATE, volume=0.5)
            env = np.exp(-8 * t)
            bass_note = 0.4 * bass_sine * env

        else:  # synth
            # Standard synth bass
            bass_sine = sine(freq, bar_duration / SAMPLE_RATE, volume=0.5)
            harmonic = sine(freq * 2, bar_duration / SAMPLE_RATE, volume=0.15)
            env = 1 - 0.4 * t / (bar_duration / SAMPLE_RATE)
            env = np.clip(env, 0, 1)
            bass_note = 0.4 * (bass_sine + harmonic) * env

        track[current_sample:current_sample + bar_duration] = bass_note
        current_sample += samples_per_bar
        bar_index += 1

    return track


def generate_chords(chord_progression: List[List[float]], tempo_bpm: float, key: str,
                    length_seconds: float, style: str = "synth") -> np.ndarray:
    """Generate chord pads.

    Args:
        chord_progression: List of chord frequency lists
        tempo_bpm: Tempo in beats per minute
        key: Musical key
        length_seconds: Total length in seconds
        style: Synth style ("dark_analog", "bright_digital", "warm_analog", "metallic", etc.)

    Returns:
        Mono pad track
    """
    num_samples = int(length_seconds * SAMPLE_RATE)
    track = np.zeros(num_samples)
    samples_per_chord = int(1 * 4 * 60 * SAMPLE_RATE / tempo_bpm)  # 1 bar per chord

    chord_index = 0
    current_sample = 0

    while current_sample < num_samples:
        chord = chord_progression[chord_index % len(chord_progression)]
        chord_duration = min(samples_per_chord, num_samples - current_sample)
        t = np.arange(chord_duration) / SAMPLE_RATE

        chord_sound = np.zeros(chord_duration)

        if style == "dark_analog":
            # Depeche Mode style - detuned saws with filter
            for freq in chord:
                saw1 = saw(freq * 0.998, chord_duration / SAMPLE_RATE, volume=0.08)
                saw2 = saw(freq, chord_duration / SAMPLE_RATE, volume=0.08)
                saw3 = saw(freq * 1.002, chord_duration / SAMPLE_RATE, volume=0.08)
                sawtooth = (saw1 + saw2 + saw3) / 3
                filter_env = 0.3 + 0.4 * np.exp(-0.5 * t)
                chord_sound += sawtooth * filter_env

        elif style == "bright_digital":
            # DX7-style FM synthesis
            for freq in chord:
                mod_freq = freq * 2.01
                mod_index = 2.0 * np.exp(-1.5 * t)
                modulation = mod_index * np.sin(2 * np.pi * mod_freq * t)
                carrier = np.sin(2 * np.pi * freq * t + modulation)
                partial1 = 0.3 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-3 * t)
                partial2 = 0.2 * np.sin(2 * np.pi * freq * 5.40 * t) * np.exp(-5 * t)
                chord_sound += 0.07 * (carrier + partial1 + partial2)

        elif style == "warm_analog":
            # Warm analog pads
            for freq in chord:
                saw1 = saw(freq * 0.999, chord_duration / SAMPLE_RATE, volume=0.09)
                saw2 = saw(freq * 1.001, chord_duration / SAMPLE_RATE, volume=0.09)
                sawtooth = (saw1 + saw2) / 2
                harmonic = sine(freq * 2, chord_duration / SAMPLE_RATE, volume=0.018)
                chord_sound += sawtooth * 0.7 + harmonic * 0.3

        elif style == "metallic":
            # Gary Numan style - ring modulation
            for freq in chord:
                carrier = sine(freq, chord_duration / SAMPLE_RATE, volume=1.0)
                modulator = sine(freq * 1.414, chord_duration / SAMPLE_RATE, volume=1.0)
                ring_mod = carrier * modulator
                metallic = ring_mod + 0.3 * sine(freq * 3.14, chord_duration / SAMPLE_RATE, volume=1.0)
                chord_sound += 0.06 * metallic

        else:  # clean/precise (Kraftwerk)
            for freq in chord:
                chord_sound += sine(freq, chord_duration / SAMPLE_RATE, volume=0.08)

        track[current_sample:current_sample + chord_duration] = chord_sound
        current_sample += samples_per_chord
        chord_index += 1

    return track


def generate_lead_melody(scale: List[float], tempo_bpm: float, key: str,
                        length_seconds: float, style: str = "synth") -> np.ndarray:
    """Generate lead melody.

    Args:
        scale: List of scale frequencies
        tempo_bpm: Tempo in beats per minute
        key: Musical key
        length_seconds: Total length in seconds
        style: Lead style

    Returns:
        Mono lead track
    """
    num_samples = int(length_seconds * SAMPLE_RATE)
    track = np.zeros(num_samples)
    samples_per_16th = int(15 * SAMPLE_RATE / tempo_bpm)

    # Simple melodic pattern
    pattern = [0, 2, 4, 2, 0, 2, 4, 5, 4, 2, 0, 2, 4, 7, 4, 0]

    step_index = 0
    current_sample = 0

    while current_sample < num_samples:
        note_idx = pattern[step_index % len(pattern)]
        freq = scale[note_idx % len(scale)]
        note_duration = min(samples_per_16th, num_samples - current_sample)

        # Square wave for classic lead sound
        lead_note = square(freq, note_duration / SAMPLE_RATE, volume=0.12, duty_cycle=0.5)

        # Plucky envelope (use actual length of lead_note to avoid broadcast errors)
        actual_length = len(lead_note)
        t = np.arange(actual_length) / SAMPLE_RATE
        env = np.exp(-20 * t)

        # Apply envelope
        lead_with_env = lead_note * env

        # Add to track
        track[current_sample:current_sample + actual_length] = lead_with_env

        current_sample += samples_per_16th
        step_index += 1

    return track


# ==================== SECTION & ARRANGEMENT LOGIC ====================

# Map section names to instrumentation
SECTION_INSTRUMENTS = {
    "intro": ["pad", "light_drums"],
    "verse": ["drums", "bass", "pad"],
    "pre_chorus": ["drums", "bass", "pad", "light_lead"],
    "chorus": ["drums", "bass", "pad", "lead"],
    "drop": ["drums", "bass", "lead"],
    "bridge": ["pad", "light_drums"],
    "outro": ["pad", "light_drums"],
    "loop": ["drums", "bass", "pad"],
}

# Section duration in bars
SECTION_DURATIONS = {
    "intro": 4,
    "verse": 8,
    "pre_chorus": 4,
    "chorus": 8,
    "drop": 8,
    "bridge": 4,
    "outro": 4,
    "loop": 16,
}


def generate_full_track(plan: ProducerPlan, track_id: str) -> np.ndarray:
    """Generate a full multi-section track based on ProducerPlan.

    Args:
        plan: ProducerPlan with tempo, key, structure, artist_style, energy_curve
        track_id: Unique track identifier

    Returns:
        Stereo audio array (n_samples, 2)
    """
    logger.info(f"Generating full track: {track_id}")
    logger.info(f"Plan: {plan.config}")

    # Extract plan parameters
    tempo_bpm = plan.config.get("tempo_bpm", 120)
    key = plan.config.get("key", "C minor")
    artist_style = plan.config.get("artist_style", "generic")
    energy_curve = plan.config.get("energy_curve", "medium")
    structure = plan.config.get("structure", ["intro", "verse", "chorus", "verse", "chorus", "outro"])
    mood = plan.config.get("mood", "neutral")

    # Determine drum style from artist
    if artist_style in ["depeche_mode", "new_order", "pet_shop_boys", "eurythmics", "kraftwerk"]:
        drum_style = "808"
    elif artist_style in ["gary_numan"]:
        drum_style = "909"
    else:
        drum_style = "808"

    # Determine bass style from artist
    if artist_style in ["gary_numan", "yazoo"]:
        bass_style = "moog"
    elif artist_style in ["depeche_mode", "kraftwerk"]:
        bass_style = "sequenced"
    elif artist_style in ["new_order", "eurythmics"]:
        bass_style = "driving"
    else:
        bass_style = "synth"

    # Determine synth style from artist
    if artist_style in ["depeche_mode", "omd"]:
        synth_style = "dark_analog"
    elif artist_style in ["pet_shop_boys", "eurythmics"]:
        synth_style = "bright_digital"
    elif artist_style in ["human_league", "tears_for_fears", "yazoo"]:
        synth_style = "warm_analog"
    elif artist_style == "gary_numan":
        synth_style = "metallic"
    else:  # kraftwerk, generic
        synth_style = "clean"

    # Build scale from key
    scale_root = 220.0  # A3
    if "A" in key:
        scale_root = 220.0
    elif "C" in key:
        scale_root = 261.63
    elif "D" in key:
        scale_root = 293.66
    elif "F" in key:
        scale_root = 349.23
    elif "G" in key:
        scale_root = 392.0

    # Build scale degrees (natural minor or major)
    if "minor" in key.lower():
        scale_degrees = [0, 2, 3, 5, 7, 8, 10, 12]  # Natural minor
    else:
        scale_degrees = [0, 2, 4, 5, 7, 9, 11, 12]  # Major

    scale = [scale_root * (2 ** (deg / 12)) for deg in scale_degrees]

    # Build chord progression
    chord_progression_root = [scale[0], scale[3], scale[1], scale[0]]

    # Build chords (root + third + fifth)
    chord_progression = []
    for root in chord_progression_root:
        if "minor" in key.lower():
            chord = [root, root * (2 ** (3/12)), root * (2 ** (7/12))]  # Minor chord
        else:
            chord = [root, root * (2 ** (4/12)), root * (2 ** (7/12))]  # Major chord
        chord_progression.append(chord)

    # Calculate total length based on structure
    total_bars = sum([SECTION_DURATIONS.get(s.lower(), 8) for s in structure])
    beats_per_bar = 4
    total_duration = total_bars * beats_per_bar * 60 / tempo_bpm

    # Cap at 60 seconds
    if total_duration > 60:
        total_duration = 60

    logger.info(f"Total duration: {total_duration:.1f}s ({total_bars} bars at {tempo_bpm} BPM)")

    num_samples = int(total_duration * SAMPLE_RATE)

    # Define drum patterns
    kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]
    snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
    hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1]

    # Adjust patterns for artist style
    if artist_style == "kraftwerk":
        # More mechanical, rigid
        hihat_pattern = [1, 0, 1, 0, 1, 0, 1, 0]
    elif artist_style in ["depeche_mode", "gary_numan"]:
        # Darker, more syncopated
        kick_pattern = [1, 0, 0, 0, 1, 0, 1, 0]

    # Generate instrument tracks
    logger.info("Generating drum tracks...")
    kick = generate_kick(kick_pattern, tempo_bpm, total_duration, style=drum_style)
    snare = generate_snare(snare_pattern, tempo_bpm, total_duration, style=drum_style)
    hihat = generate_hihat(hihat_pattern, tempo_bpm, total_duration)

    logger.info("Generating bassline...")
    bass = generate_bassline(chord_progression_root, tempo_bpm, key, total_duration, style=bass_style)

    logger.info("Generating chord pads...")
    pads = generate_chords(chord_progression, tempo_bpm, key, total_duration, style=synth_style)

    logger.info("Generating lead melody...")
    lead = generate_lead_melody(scale, tempo_bpm, key, total_duration, style="synth")

    # Section-based mixing
    logger.info("Mixing sections...")
    mix = np.zeros(num_samples)

    samples_per_bar = int(beats_per_bar * 60 * SAMPLE_RATE / tempo_bpm)
    current_sample = 0

    for section_name in structure:
        section_lower = section_name.lower()
        section_bars = SECTION_DURATIONS.get(section_lower, 8)
        section_samples = section_bars * samples_per_bar

        # Prevent overflow
        if current_sample + section_samples > num_samples:
            section_samples = num_samples - current_sample

        if section_samples <= 0:
            break

        end_sample = current_sample + section_samples

        # Determine which instruments play in this section
        instruments = SECTION_INSTRUMENTS.get(section_lower, ["drums", "bass", "pad"])

        # Mix instruments based on section
        # Ensure we don't exceed the length of the instrument tracks
        actual_end = min(end_sample, len(kick), len(snare), len(hihat), len(bass), len(pads), len(lead))
        section_length = actual_end - current_sample

        if section_length > 0:
            if "drums" in instruments or "light_drums" in instruments:
                drum_volume = 0.5 if "light_drums" in instruments else 1.0
                mix[current_sample:actual_end] += kick[current_sample:actual_end] * drum_volume
                mix[current_sample:actual_end] += snare[current_sample:actual_end] * drum_volume
                mix[current_sample:actual_end] += hihat[current_sample:actual_end] * drum_volume * 0.7

            if "bass" in instruments:
                mix[current_sample:actual_end] += bass[current_sample:actual_end]

            if "pad" in instruments:
                mix[current_sample:actual_end] += pads[current_sample:actual_end]

            if "lead" in instruments or "light_lead" in instruments:
                lead_volume = 0.6 if "light_lead" in instruments else 1.0
                mix[current_sample:actual_end] += lead[current_sample:actual_end] * lead_volume

        current_sample = end_sample

    # Apply sidechain compression if appropriate
    if artist_style in ["depeche_mode", "new_order", "pet_shop_boys", "eurythmics"]:
        logger.info("Applying sidechain compression...")
        kick_envelope = np.abs(kick)
        window = int(0.05 * SAMPLE_RATE)
        if window > 0:
            kick_envelope = np.convolve(kick_envelope, np.ones(window) / window, mode='same')
        sidechain = 1 - 0.4 * (kick_envelope / (np.max(kick_envelope) + 1e-6))
        sidechain = np.clip(sidechain, 0.3, 1.0)
        mix = mix * sidechain

    # Normalize to prevent clipping
    max_val = np.max(np.abs(mix))
    if max_val > 0:
        mix = mix / max_val * 0.85

    # Apply fade in/out
    fade_samples = int(0.5 * SAMPLE_RATE)
    if len(mix) > fade_samples * 2:
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        mix[:fade_samples] *= fade_in
        mix[-fade_samples:] *= fade_out

    # Convert to stereo
    stereo = np.column_stack([mix, mix])

    # Apply simple stereo widening to pads
    if len(pads) == len(mix):
        # Delay right channel slightly for width
        delay_samples = int(0.015 * SAMPLE_RATE)
        pads_right = np.concatenate([np.zeros(delay_samples), pads[:-delay_samples]])
        stereo[:, 1] += pads_right * 0.15  # Subtle width effect

    logger.info(f"Track generation complete: {len(stereo) / SAMPLE_RATE:.1f}s")

    return stereo
