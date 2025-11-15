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


class PremiumMusicEngine:
    """
    Premium artist-influenced procedural music engine.

    Generates high-quality electronic/synthwave backing tracks with:
    - Artist-specific sound characteristics
    - Authentic 808/909/LinnDrum synthesis
    - ADSR envelopes and filter sweeps
    - Advanced production techniques (sidechain, gated reverb)
    - Era-specific production styles
    """

    SAMPLE_RATE = 44100

    # Premium Artist Database (10 artists from 80s electronic/synthwave era)
    ARTIST_DATABASE = {
        "depeche_mode": {
            "name": "Depeche Mode",
            "tempo_range": (110, 125),
            "scales": [[55, 65.4, 73.4, 77.8, 87.3, 98]],  # A minor (dark)
            "instruments": ["analog_synth", "808", "sequencer", "bass_synth"],
            "production_era": "mid_80s_digital",
            "mood": "dark",
            "characteristics": {
                "bass_style": "sequenced",
                "synth_type": "dark_analog",
                "drum_machine": "808",
                "use_sidechain": True,
                "use_gated_reverb": True,
            }
        },
        "gary_numan": {
            "name": "Gary Numan",
            "tempo_range": (115, 130),
            "scales": [[49, 58.3, 65.4, 73.4, 77.8, 87.3]],  # G minor (dystopian)
            "instruments": ["moog", "prophet5", "909", "arpeggiator"],
            "production_era": "early_80s_analog",
            "mood": "dystopian",
            "characteristics": {
                "bass_style": "analog_moog",
                "synth_type": "metallic",
                "drum_machine": "909",
                "use_sidechain": False,
                "use_gated_reverb": False,
            }
        },
        "kraftwerk": {
            "name": "Kraftwerk",
            "tempo_range": (120, 130),
            "scales": [[65.4, 73.4, 82.4, 87.3, 98, 110]],  # C major (robotic)
            "instruments": ["vocoder", "808", "sequencer", "arpeggiator"],
            "production_era": "early_80s_analog",
            "mood": "mechanical",
            "characteristics": {
                "bass_style": "sequenced",
                "synth_type": "precise",
                "drum_machine": "808",
                "use_sidechain": False,
                "use_gated_reverb": False,
            }
        },
        "new_order": {
            "name": "New Order",
            "tempo_range": (115, 128),
            "scales": [[55, 61.7, 65.4, 73.4, 82.4, 87.3]],  # A minor (upbeat)
            "instruments": ["dx7", "808", "sequencer", "bass_guitar"],
            "production_era": "mid_80s_digital",
            "mood": "melancholic",
            "characteristics": {
                "bass_style": "driving",
                "synth_type": "bright_digital",
                "drum_machine": "808",
                "use_sidechain": True,
                "use_gated_reverb": True,
            }
        },
        "pet_shop_boys": {
            "name": "Pet Shop Boys",
            "tempo_range": (118, 125),
            "scales": [[58.3, 65.4, 73.4, 77.8, 87.3, 98]],  # Bb major (pop)
            "instruments": ["dx7", "linn_drum", "sequencer", "bass_synth"],
            "production_era": "mid_80s_digital",
            "mood": "sophisticated",
            "characteristics": {
                "bass_style": "synth_bass",
                "synth_type": "polished_digital",
                "drum_machine": "linn_drum",
                "use_sidechain": True,
                "use_gated_reverb": True,
            }
        },
        "human_league": {
            "name": "The Human League",
            "tempo_range": (110, 120),
            "scales": [[65.4, 69.3, 73.4, 82.4, 87.3, 98]],  # C major (romantic)
            "instruments": ["roland_system", "linn_drum", "sequencer", "bass_synth"],
            "production_era": "early_80s_analog",
            "mood": "romantic",
            "characteristics": {
                "bass_style": "synth_bass",
                "synth_type": "warm_analog",
                "drum_machine": "linn_drum",
                "use_sidechain": False,
                "use_gated_reverb": True,
            }
        },
        "omd": {
            "name": "Orchestral Manoeuvres in the Dark",
            "tempo_range": (115, 125),
            "scales": [[49, 58.3, 61.7, 69.3, 77.8, 87.3]],  # G minor (atmospheric)
            "instruments": ["mellotron", "808", "sequencer", "bass_synth"],
            "production_era": "early_80s_analog",
            "mood": "atmospheric",
            "characteristics": {
                "bass_style": "melodic",
                "synth_type": "orchestral",
                "drum_machine": "808",
                "use_sidechain": False,
                "use_gated_reverb": True,
            }
        },
        "tears_for_fears": {
            "name": "Tears for Fears",
            "tempo_range": (100, 115),
            "scales": [[55, 61.7, 65.4, 73.4, 77.8, 87.3]],  # A minor (emotive)
            "instruments": ["prophet5", "linn_drum", "arpeggiator", "bass_synth"],
            "production_era": "mid_80s_digital",
            "mood": "emotive",
            "characteristics": {
                "bass_style": "powerful",
                "synth_type": "lush_analog",
                "drum_machine": "linn_drum",
                "use_sidechain": True,
                "use_gated_reverb": True,
            }
        },
        "eurythmics": {
            "name": "Eurythmics",
            "tempo_range": (108, 122),
            "scales": [[58.3, 65.4, 69.3, 77.8, 82.4, 92.5]],  # Bb major (powerful)
            "instruments": ["dx7", "808", "sequencer", "bass_synth"],
            "production_era": "mid_80s_digital",
            "mood": "powerful",
            "characteristics": {
                "bass_style": "driving",
                "synth_type": "sharp_digital",
                "drum_machine": "808",
                "use_sidechain": True,
                "use_gated_reverb": True,
            }
        },
        "yazoo": {
            "name": "Yazoo",
            "tempo_range": (112, 125),
            "scales": [[65.4, 73.4, 77.8, 82.4, 87.3, 98]],  # C major (uplifting)
            "instruments": ["moog", "808", "sequencer", "bass_synth"],
            "production_era": "early_80s_analog",
            "mood": "uplifting",
            "characteristics": {
                "bass_style": "analog_moog",
                "synth_type": "warm_analog",
                "drum_machine": "808",
                "use_sidechain": False,
                "use_gated_reverb": False,
            }
        },
    }

    # Preset Kits for Beta (not artist-specific names, but style-specific)
    PRESET_KITS = {
        "dark_synthpop": {
            "artists": ["depeche_mode", "gary_numan"],
            "instruments": ["analog_synth", "808", "sequencer"],
            "mood": "dark",
            "production_era": "mid_80s_digital",
        },
        "new_romantic": {
            "artists": ["human_league", "tears_for_fears"],
            "instruments": ["prophet5", "linn_drum", "arpeggiator"],
            "mood": "romantic",
            "production_era": "early_80s_analog",
        },
        "electro_pop": {
            "artists": ["pet_shop_boys", "eurythmics"],
            "instruments": ["dx7", "808", "sequencer"],
            "mood": "sophisticated",
            "production_era": "mid_80s_digital",
        },
        "synth_wave": {
            "artists": ["kraftwerk", "new_order"],
            "instruments": ["sequencer", "808", "bass_synth"],
            "mood": "mechanical",
            "production_era": "early_80s_analog",
        },
        "darkwave": {
            "artists": ["omd", "gary_numan"],
            "instruments": ["mellotron", "808", "bass_synth"],
            "mood": "atmospheric",
            "production_era": "early_80s_analog",
        },
    }

    def generate_backing_track(self, request: MusicGenerateRequest) -> str:
        """
        Generate premium artist-influenced backing track.

        Args:
            request: Music generation request with artist_influences, instruments, etc.

        Returns:
            URL path to the generated audio file
        """
        try:
            # Resolve artist influences to musical parameters
            params = self._resolve_artist_params(request)

            # Get tempo (auto-detect from artist if not provided)
            tempo_bpm = request.tempo_bpm or params["tempo_bpm"]

            # Calculate timing
            bars = 8
            beats_per_bar = 4
            duration_seconds = bars * beats_per_bar * 60 / tempo_bpm
            num_samples = int(duration_seconds * self.SAMPLE_RATE)

            # Generate premium track components based on drum machine type
            kick = self._generate_premium_kick(
                num_samples, tempo_bpm,
                params["kick_pattern"],
                params["drum_machine"]
            )
            snare = self._generate_premium_snare(
                num_samples, tempo_bpm,
                params["snare_pattern"],
                params["drum_machine"]
            )
            hihat = self._generate_premium_hihat(
                num_samples, tempo_bpm,
                params["hihat_pattern"],
                params["drum_machine"]
            )

            # Generate bass based on artist style
            bass = self._generate_premium_bass(
                num_samples, tempo_bpm,
                params["scale"],
                params["bass_style"],
                params["bass_intensity"]
            )

            # Generate synth layers based on synth type
            synth = self._generate_premium_synth(
                num_samples, tempo_bpm,
                params["scale"],
                params["synth_type"]
            )

            # Add arpeggiator if in instruments
            if "arpeggiator" in params["instruments"]:
                arp = self._generate_arpeggiator(
                    num_samples, tempo_bpm, params["scale"]
                )
                mix = kick + snare + hihat + bass + synth + arp
            else:
                mix = kick + snare + hihat + bass + synth

            # Apply sidechain compression if enabled
            if params["use_sidechain"]:
                mix = self._apply_sidechain(mix, kick, strength=0.4)

            # Apply gated reverb if enabled
            if params["use_gated_reverb"]:
                snare = self._apply_gated_reverb(snare, gate_time=0.15)
                # Re-mix with processed snare
                mix = kick + snare + hihat + bass + synth
                if "arpeggiator" in params["instruments"]:
                    mix = mix + arp

            # Normalize to prevent clipping
            max_val = np.max(np.abs(mix))
            if max_val > 0:
                mix = mix / max_val * 0.85  # Leave headroom

            # Apply fade in/out
            fade_samples = int(0.5 * self.SAMPLE_RATE)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            mix[:fade_samples] *= fade_in
            mix[-fade_samples:] *= fade_out

            # Generate track ID
            track_input = f"{'_'.join(request.artist_influences)}{request.mood or ''}{request.reference_text or ''}"
            track_id = hashlib.md5(track_input.encode()).hexdigest()[:12]

            # Save to file
            filename = f"track-{track_id}.wav"
            file_path = AUDIO_DIR / filename
            sf.write(str(file_path), mix, self.SAMPLE_RATE)

            logger.info(
                f"Generated premium track: {track_id} "
                f"(artists={', '.join(request.artist_influences)}, "
                f"{tempo_bpm} BPM, {duration_seconds:.1f}s)"
            )

            return f"/static/audio/music/{filename}"

        except Exception as e:
            logger.error(f"Failed to generate premium music: {e}")
            raise

    def _resolve_artist_params(self, request: MusicGenerateRequest) -> Dict[str, Any]:
        """
        Resolve artist influences to concrete musical parameters.

        Combines characteristics from multiple artists and applies overrides.
        """
        # Normalize artist names to database keys
        artist_keys = []
        for artist in request.artist_influences:
            # Convert "Depeche Mode" -> "depeche_mode"
            key = artist.lower().replace(" ", "_").replace("the_", "")
            if key in self.ARTIST_DATABASE:
                artist_keys.append(key)

        # Fallback to default if no valid artists
        if not artist_keys:
            artist_keys = ["depeche_mode"]  # Default to Depeche Mode

        # Get primary artist (first in list)
        primary = self.ARTIST_DATABASE[artist_keys[0]]

        # Merge characteristics from multiple artists
        merged_instruments = set(primary["instruments"])
        merged_scales = primary["scales"]

        for key in artist_keys[1:]:
            artist = self.ARTIST_DATABASE[key]
            merged_instruments.update(artist["instruments"])

        # Override instruments if user specified
        if request.instruments:
            final_instruments = request.instruments
        else:
            final_instruments = list(merged_instruments)

        # Override mood if user specified
        final_mood = request.mood or primary["mood"]

        # Override production_era if user specified
        final_era = request.production_era or primary["production_era"]

        # Select scale (use primary artist's scale)
        scale = merged_scales[0]

        # Determine tempo (average of all artists' ranges)
        tempo_ranges = [self.ARTIST_DATABASE[k]["tempo_range"] for k in artist_keys]
        avg_min = int(np.mean([r[0] for r in tempo_ranges]))
        avg_max = int(np.mean([r[1] for r in tempo_ranges]))
        default_tempo = (avg_min + avg_max) // 2

        # Determine drum patterns based on mood and era
        kick_pattern, snare_pattern, hihat_pattern = self._get_drum_patterns(final_mood, final_era)

        # Determine drum machine
        drum_machine = primary["characteristics"]["drum_machine"]

        # Determine bass style and intensity
        bass_style = primary["characteristics"]["bass_style"]
        bass_intensity = 0.4 if "powerful" in final_mood else 0.35

        # Determine synth type
        synth_type = primary["characteristics"]["synth_type"]

        return {
            "artist_keys": artist_keys,
            "instruments": final_instruments,
            "scale": scale,
            "tempo_bpm": default_tempo,
            "mood": final_mood,
            "production_era": final_era,
            "kick_pattern": kick_pattern,
            "snare_pattern": snare_pattern,
            "hihat_pattern": hihat_pattern,
            "drum_machine": drum_machine,
            "bass_style": bass_style,
            "bass_intensity": bass_intensity,
            "synth_type": synth_type,
            "use_sidechain": primary["characteristics"]["use_sidechain"],
            "use_gated_reverb": primary["characteristics"]["use_gated_reverb"],
        }

    def _get_drum_patterns(self, mood: str, era: str) -> tuple:
        """Get era and mood-appropriate drum patterns."""
        # Dark/dystopian moods
        if mood in ["dark", "dystopian", "atmospheric"]:
            kick_pattern = [1, 0, 0, 0, 1, 0, 1, 0]
            snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
            hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1]
        # Uplifting/romantic moods
        elif mood in ["uplifting", "romantic", "emotive"]:
            kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]
            snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
            hihat_pattern = [0, 1, 0, 1, 0, 1, 0, 1]
        # Mechanical/precise moods
        elif mood in ["mechanical", "sophisticated"]:
            kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]
            snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
            hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1]
        # Default pattern
        else:
            kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]
            snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
            hihat_pattern = [0, 1, 0, 1, 0, 1, 0, 1]

        return kick_pattern, snare_pattern, hihat_pattern

    # ========== PREMIUM DRUM SYNTHESIS ==========

    def _generate_premium_kick(
        self, num_samples: int, tempo_bpm: float,
        pattern: List[int], drum_machine: str
    ) -> np.ndarray:
        """Generate authentic 808/909/LinnDrum kick."""
        track = np.zeros(num_samples)
        samples_per_beat = int(60 * self.SAMPLE_RATE / tempo_bpm)

        beat_index = 0
        current_sample = 0

        while current_sample < num_samples:
            if pattern[beat_index % len(pattern)] == 1:
                if drum_machine == "808":
                    kick = self._808_kick()
                elif drum_machine == "909":
                    kick = self._909_kick()
                else:  # linn_drum
                    kick = self._linn_kick()

                end_sample = min(current_sample + len(kick), num_samples)
                actual_duration = end_sample - current_sample
                track[current_sample:end_sample] += kick[:actual_duration]

            current_sample += samples_per_beat
            beat_index += 1

        return track

    def _808_kick(self) -> np.ndarray:
        """Authentic TR-808 kick - deep, boomy, long decay."""
        duration = int(0.4 * self.SAMPLE_RATE)  # Longer for 808 character
        t = np.arange(duration) / self.SAMPLE_RATE

        # Deep pitch envelope (frequency sweep from 180Hz down to 35Hz)
        freq_start = 180
        freq_end = 35
        freq_env = freq_start * np.exp(-6 * t) + freq_end

        # Slower amplitude envelope for that boomy character
        amp_env = np.exp(-4.5 * t)

        # Sine oscillator with pitch envelope
        phase = 2 * np.pi * np.cumsum(freq_env) / self.SAMPLE_RATE
        kick = 1.0 * np.sin(phase) * amp_env

        # Add sub-harmonic for extra depth
        sub_freq_env = freq_env * 0.5
        sub_phase = 2 * np.pi * np.cumsum(sub_freq_env) / self.SAMPLE_RATE
        kick += 0.3 * np.sin(sub_phase) * amp_env

        # Sharp attack click (classic 808 characteristic)
        click_duration = int(0.002 * self.SAMPLE_RATE)
        click = np.zeros(duration)
        click[:click_duration] = np.exp(-500 * t[:click_duration]) * 0.15

        # Combine with some noise for texture
        noise = np.random.randn(duration) * np.exp(-50 * t) * 0.05

        return kick + click + noise

    def _909_kick(self) -> np.ndarray:
        """Authentic TR-909 kick - punchy, tight, with pronounced click."""
        duration = int(0.18 * self.SAMPLE_RATE)  # Tighter than 808
        t = np.arange(duration) / self.SAMPLE_RATE

        # Sharp pitch envelope (909 is punchier)
        freq_start = 220
        freq_end = 55
        freq_env = freq_start * np.exp(-12 * t) + freq_end

        # Very tight amplitude envelope
        amp_env = np.exp(-10 * t)

        # Sine oscillator with some distortion
        phase = 2 * np.pi * np.cumsum(freq_env) / self.SAMPLE_RATE
        kick = 0.95 * np.sin(phase) * amp_env

        # Add slight harmonic distortion for punch
        kick += 0.15 * np.sin(2 * phase) * amp_env * np.exp(-15 * t)

        # Very pronounced click (909 signature)
        click_duration = int(0.003 * self.SAMPLE_RATE)
        click = np.zeros(duration)
        click_env = np.exp(-600 * t[:click_duration])
        click[:click_duration] = np.random.randn(click_duration) * click_env * 0.25

        return kick + click

    def _linn_kick(self) -> np.ndarray:
        """LinnDrum kick - natural, sample-like, less synthetic."""
        duration = int(0.22 * self.SAMPLE_RATE)
        t = np.arange(duration) / self.SAMPLE_RATE

        # More moderate pitch envelope (natural acoustic kick behavior)
        freq_start = 140
        freq_end = 50
        freq_env = freq_start * np.exp(-7 * t) + freq_end

        # Natural decay curve
        amp_env = np.exp(-6 * t)

        # Sine with slight harmonics for realism
        phase = 2 * np.pi * np.cumsum(freq_env) / self.SAMPLE_RATE
        kick = 0.85 * np.sin(phase) * amp_env
        kick += 0.1 * np.sin(1.5 * phase) * amp_env  # Slight overtone

        # Softer attack transient (more acoustic)
        attack_duration = int(0.005 * self.SAMPLE_RATE)
        attack = np.zeros(duration)
        attack[:attack_duration] = np.linspace(0, 1, attack_duration) ** 0.5
        attack[attack_duration:] = 1
        kick = kick * attack

        # Add subtle noise for texture (simulating beater hit)
        noise = np.random.randn(duration) * np.exp(-30 * t) * 0.08

        return kick + noise

    def _generate_premium_snare(
        self, num_samples: int, tempo_bpm: float,
        pattern: List[int], drum_machine: str
    ) -> np.ndarray:
        """Generate authentic snare based on drum machine."""
        track = np.zeros(num_samples)
        samples_per_beat = int(60 * self.SAMPLE_RATE / tempo_bpm)

        beat_index = 0
        current_sample = 0

        while current_sample < num_samples:
            if pattern[beat_index % len(pattern)] == 1:
                if drum_machine == "808":
                    snare = self._808_snare()
                elif drum_machine == "909":
                    snare = self._909_snare()
                else:  # linn_drum
                    snare = self._linn_snare()

                end_sample = min(current_sample + len(snare), num_samples)
                actual_duration = end_sample - current_sample
                track[current_sample:end_sample] += snare[:actual_duration]

            current_sample += samples_per_beat
            beat_index += 1

        return track

    def _808_snare(self) -> np.ndarray:
        """Authentic TR-808 snare (metallic, filtered noise)."""
        duration = int(0.15 * self.SAMPLE_RATE)
        t = np.arange(duration) / self.SAMPLE_RATE

        # Two oscillators at dissonant frequencies
        tone1 = np.sin(2 * np.pi * 180 * t)
        tone2 = np.sin(2 * np.pi * 330 * t)

        # White noise component
        noise = np.random.randn(duration)

        # Envelope
        envelope = np.exp(-25 * t)

        # Mix (808 is more tonal than other snares)
        snare = 0.4 * (0.6 * (tone1 + tone2) + 0.4 * noise) * envelope

        return snare

    def _909_snare(self) -> np.ndarray:
        """Authentic TR-909 snare (crisp, bright)."""
        duration = int(0.12 * self.SAMPLE_RATE)
        t = np.arange(duration) / self.SAMPLE_RATE

        # Tonal component (single oscillator)
        tone = np.sin(2 * np.pi * 200 * t)

        # White noise (more prominent)
        noise = np.random.randn(duration)

        # Sharp envelope
        envelope = np.exp(-30 * t)

        # Mix (909 is noisier and crisper)
        snare = 0.45 * (0.3 * tone + 0.7 * noise) * envelope

        return snare

    def _linn_snare(self) -> np.ndarray:
        """LinnDrum snare (natural, less synthetic)."""
        duration = int(0.18 * self.SAMPLE_RATE)
        t = np.arange(duration) / self.SAMPLE_RATE

        # Natural-sounding noise
        noise = np.random.randn(duration)

        # Gentle tonal component
        tone = np.sin(2 * np.pi * 220 * t)

        # Natural envelope
        envelope = np.exp(-15 * t)

        # Mix (more natural balance)
        snare = 0.4 * (0.25 * tone + 0.75 * noise) * envelope

        return snare

    def _generate_premium_hihat(
        self, num_samples: int, tempo_bpm: float,
        pattern: List[int], drum_machine: str
    ) -> np.ndarray:
        """Generate authentic hi-hat."""
        track = np.zeros(num_samples)
        samples_per_beat = int(60 * self.SAMPLE_RATE / tempo_bpm)

        beat_index = 0
        current_sample = 0

        while current_sample < num_samples:
            if pattern[beat_index % len(pattern)] == 1:
                # All drum machines have similar hi-hats (metallic noise)
                hihat_duration = int(0.06 * self.SAMPLE_RATE)
                noise = np.random.randn(hihat_duration)

                # High-pass filter (simple differentiation)
                hihat = np.diff(noise, prepend=0)

                # Sharp decay
                envelope = np.exp(-60 * np.arange(hihat_duration) / self.SAMPLE_RATE)
                hihat = 0.18 * hihat * envelope

                end_sample = min(current_sample + hihat_duration, num_samples)
                actual_duration = end_sample - current_sample
                track[current_sample:end_sample] += hihat[:actual_duration]

            current_sample += samples_per_beat
            beat_index += 1

        return track

    # ========== PREMIUM BASS SYNTHESIS ==========

    def _generate_premium_bass(
        self, num_samples: int, tempo_bpm: float,
        scale: List[float], bass_style: str, intensity: float
    ) -> np.ndarray:
        """Generate premium bass based on style."""
        if bass_style == "analog_moog":
            return self._moog_bass(num_samples, tempo_bpm, scale, intensity)
        elif bass_style == "sequenced":
            return self._sequenced_bass(num_samples, tempo_bpm, scale, intensity)
        elif bass_style == "driving":
            return self._driving_bass(num_samples, tempo_bpm, scale, intensity)
        else:  # synth_bass, melodic, powerful
            return self._synth_bass(num_samples, tempo_bpm, scale, intensity)

    def _moog_bass(
        self, num_samples: int, tempo_bpm: float,
        scale: List[float], intensity: float
    ) -> np.ndarray:
        """Moog-style analog bass - fat, rich, filter sweep, slight detuning."""
        track = np.zeros(num_samples)
        samples_per_bar = int(4 * 60 * self.SAMPLE_RATE / tempo_bpm)

        # Dark minor progression
        progression = [scale[0], scale[2], scale[1], scale[0]]

        bar_index = 0
        current_sample = 0

        while current_sample < num_samples:
            freq = progression[bar_index % len(progression)]
            bar_duration = min(samples_per_bar, num_samples - current_sample)
            t = np.arange(bar_duration) / self.SAMPLE_RATE

            # Triple sawtooth with slight detuning for FAT sound
            saw1 = 2 * (t * freq % 1) - 1
            saw2 = 2 * (t * freq * 1.005 % 1) - 1  # Slightly sharp
            saw3 = 2 * (t * freq * 0.995 % 1) - 1  # Slightly flat
            sawtooth = (saw1 + saw2 + saw3) / 3

            # ADSR envelope
            attack = int(0.005 * self.SAMPLE_RATE)  # Very fast attack
            decay = int(0.15 * self.SAMPLE_RATE)
            sustain_level = 0.65
            release = int(0.25 * self.SAMPLE_RATE)

            envelope = np.ones(bar_duration)
            if len(envelope) > attack:
                envelope[:attack] = np.linspace(0, 1, attack)
            if len(envelope) > attack + decay:
                envelope[attack:attack + decay] = np.linspace(1, sustain_level, decay)
                if len(envelope) > attack + decay + release:
                    envelope[attack + decay:-release] = sustain_level
                    envelope[-release:] = np.linspace(sustain_level, 0, release)

            # Resonant low-pass filter simulation (time-varying)
            cutoff_envelope = 0.2 + 0.8 * np.exp(-5 * t)  # Opens then closes
            filtered = sawtooth * cutoff_envelope + sawtooth * (1 - cutoff_envelope) * 0.3

            # Add sub-bass for that Moog depth
            sub = np.sin(2 * np.pi * freq * 0.5 * t)

            bass_note = intensity * (filtered * 0.7 + sub * 0.3) * envelope

            track[current_sample:current_sample + bar_duration] = bass_note

            current_sample += samples_per_bar
            bar_index += 1

        return track

    def _sequenced_bass(
        self, num_samples: int, tempo_bpm: float,
        scale: List[float], intensity: float
    ) -> np.ndarray:
        """Sequenced bass - plucky square wave with rapid decay (Depeche Mode style)."""
        track = np.zeros(num_samples)
        samples_per_16th = int(15 * self.SAMPLE_RATE / tempo_bpm)

        # Bassline pattern (16ths) - more rhythmic
        note_pattern = [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0]

        step_index = 0
        current_sample = 0

        while current_sample < num_samples:
            note_idx = note_pattern[step_index % len(note_pattern)]
            if note_idx > 0:
                freq = scale[note_idx % len(scale)]
                note_duration = min(samples_per_16th, num_samples - current_sample)
                t = np.arange(note_duration) / self.SAMPLE_RATE

                # Pulse wave (adjustable duty cycle for variation)
                duty_cycle = 0.25  # Narrow pulse for sharper sound
                pulse = np.where((t * freq % 1) < duty_cycle, 1, -1)

                # Very short, plucky envelope
                envelope = np.exp(-20 * t)

                # Add slight pitch bend down for pluck character
                pitch_bend = np.exp(-30 * t) * 0.02  # Small pitch drop
                freq_modulated = freq * (1 - pitch_bend)
                pulse = np.where((t * freq_modulated % 1) < duty_cycle, 1, -1)

                bass_note = intensity * 0.6 * pulse * envelope

                end_sample = min(current_sample + note_duration, num_samples)
                track[current_sample:end_sample] += bass_note[:end_sample - current_sample]

            current_sample += samples_per_16th
            step_index += 1

        return track

    def _driving_bass(
        self, num_samples: int, tempo_bpm: float,
        scale: List[float], intensity: float
    ) -> np.ndarray:
        """Driving bass (8th notes)."""
        track = np.zeros(num_samples)
        samples_per_8th = int(30 * self.SAMPLE_RATE / tempo_bpm)

        # Driving pattern
        note_pattern = [0, 0, 0, 2, 0, 0, 2, 0]

        step_index = 0
        current_sample = 0

        while current_sample < num_samples:
            note_idx = note_pattern[step_index % len(note_pattern)]
            freq = scale[note_idx % len(scale)]
            note_duration = min(samples_per_8th, num_samples - current_sample)
            t = np.arange(note_duration) / self.SAMPLE_RATE

            # Sine wave
            sine = np.sin(2 * np.pi * freq * t)

            # Envelope
            envelope = np.exp(-8 * t)

            bass_note = intensity * sine * envelope

            track[current_sample:current_sample + note_duration] = bass_note

            current_sample += samples_per_8th
            step_index += 1

        return track

    def _synth_bass(
        self, num_samples: int, tempo_bpm: float,
        scale: List[float], intensity: float
    ) -> np.ndarray:
        """Standard synth bass."""
        track = np.zeros(num_samples)
        samples_per_bar = int(4 * 60 * self.SAMPLE_RATE / tempo_bpm)

        progression = [scale[0], scale[4], scale[2], scale[3]]

        bar_index = 0
        current_sample = 0

        while current_sample < num_samples:
            freq = progression[bar_index % len(progression)]
            bar_duration = min(samples_per_bar, num_samples - current_sample)
            t = np.arange(bar_duration) / self.SAMPLE_RATE

            # Sine wave with slight harmonic
            bass_note = intensity * (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t))

            # Envelope
            envelope = 1 - 0.4 * t / (bar_duration / self.SAMPLE_RATE)
            envelope = np.clip(envelope, 0, 1)

            track[current_sample:current_sample + bar_duration] = bass_note * envelope

            current_sample += samples_per_bar
            bar_index += 1

        return track

    # ========== PREMIUM SYNTH SYNTHESIS ==========

    def _generate_premium_synth(
        self, num_samples: int, tempo_bpm: float,
        scale: List[float], synth_type: str
    ) -> np.ndarray:
        """Generate premium synth pads/chords with dramatically different character per type."""
        track = np.zeros(num_samples)
        samples_per_2bars = int(8 * 60 * self.SAMPLE_RATE / tempo_bpm)

        # Chord progressions
        chords = [
            [scale[0], scale[2], scale[4]],  # i
            [scale[3], scale[5], scale[1]],  # VI
        ]

        chord_index = 0
        current_sample = 0

        while current_sample < num_samples:
            chord = chords[chord_index % len(chords)]
            chord_duration = min(samples_per_2bars, num_samples - current_sample)
            t = np.arange(chord_duration) / self.SAMPLE_RATE

            chord_sound = np.zeros(chord_duration)

            # DRAMATICALLY different synth types
            if synth_type == "dark_analog":
                # Dark analog: Detuned sawtooth, slow filter, chorus effect
                for i, freq in enumerate(chord):
                    # Triple-layer detuned sawtooths
                    saw1 = 2 * (t * freq * 0.998 % 1) - 1
                    saw2 = 2 * (t * freq * 1.000 % 1) - 1
                    saw3 = 2 * (t * freq * 1.002 % 1) - 1
                    sawtooth = (saw1 + saw2 + saw3) / 3

                    # Slow filter sweep (darker over time)
                    filter_env = 0.3 + 0.4 * np.exp(-0.5 * t)

                    chord_sound += 0.08 * sawtooth * filter_env

            elif synth_type == "bright_digital" or synth_type == "polished_digital" or synth_type == "sharp_digital":
                # Bright digital: DX7-style FM synthesis simulation
                for freq in chord:
                    # Carrier and modulator for FM-like sound
                    modulator_freq = freq * 2.01
                    modulation_index = 2.0 * np.exp(-1.5 * t)  # Decays over time
                    modulation = modulation_index * np.sin(2 * np.pi * modulator_freq * t)

                    # Carrier frequency modulated by modulator
                    carrier = np.sin(2 * np.pi * freq * t + modulation)

                    # Add bell-like partials
                    partial1 = 0.3 * np.sin(2 * np.pi * freq * 2.76 * t)
                    partial2 = 0.2 * np.sin(2 * np.pi * freq * 5.40 * t)

                    digital_sound = carrier + partial1 * np.exp(-3 * t) + partial2 * np.exp(-5 * t)
                    chord_sound += 0.07 * digital_sound

            elif synth_type == "warm_analog" or synth_type == "lush_analog":
                # Warm analog: Smooth sawtooth with chorus and warmth
                for freq in chord:
                    # Dual sawtooth with slight detuning
                    saw1 = 2 * (t * freq * 0.999 % 1) - 1
                    saw2 = 2 * (t * freq * 1.001 % 1) - 1
                    sawtooth = (saw1 + saw2) / 2

                    # Warm filter (always open)
                    # Add subtle harmonics for warmth
                    harmonic = 0.2 * np.sin(2 * np.pi * freq * 2 * t)

                    chord_sound += 0.09 * (sawtooth * 0.7 + harmonic * 0.3)

            elif synth_type == "metallic":
                # Metallic: Ring modulation, harsh harmonics (Gary Numan style)
                for freq in chord:
                    # Ring modulation effect
                    carrier = np.sin(2 * np.pi * freq * t)
                    modulator = np.sin(2 * np.pi * freq * 1.414 * t)  # Inharmonic ratio
                    ring_mod = carrier * modulator

                    # Add metallic partials
                    metallic = ring_mod + 0.3 * np.sin(2 * np.pi * freq * 3.14 * t)

                    chord_sound += 0.06 * metallic

            elif synth_type == "orchestral":
                # Orchestral: String-like with slow attack
                for freq in chord:
                    # Slow attack envelope
                    attack_time = 0.3  # 300ms attack
                    attack_samples = int(attack_time * self.SAMPLE_RATE)
                    attack_env = np.ones(chord_duration)
                    if chord_duration > attack_samples:
                        attack_env[:attack_samples] = np.linspace(0, 1, attack_samples) ** 2

                    # String-like sound (filtered sawtooth)
                    sawtooth = 2 * (t * freq % 1) - 1
                    # Soft filter
                    filtered = sawtooth * 0.4 + np.sin(2 * np.pi * freq * t) * 0.6

                    chord_sound += 0.08 * filtered * attack_env

            else:  # Default: precise, clean
                # Clean sine waves (Kraftwerk style)
                for freq in chord:
                    sine = np.sin(2 * np.pi * freq * t)
                    chord_sound += 0.08 * sine

            # Add subtle vibrato (except for digital/precise types)
            if "digital" not in synth_type and "precise" not in synth_type and "metallic" not in synth_type:
                vibrato = 0.004 * np.sin(2 * np.pi * 5.3 * t)
                for freq in chord:
                    chord_sound += 0.015 * np.sin(2 * np.pi * freq * t * (1 + vibrato))

            track[current_sample:current_sample + chord_duration] = chord_sound

            current_sample += samples_per_2bars
            chord_index += 1

        return track

    def _generate_arpeggiator(
        self, num_samples: int, tempo_bpm: float, scale: List[float]
    ) -> np.ndarray:
        """Generate arpeggiated sequence."""
        track = np.zeros(num_samples)
        samples_per_16th = int(15 * self.SAMPLE_RATE / tempo_bpm)

        # Arpeggio pattern (up and down)
        arp_pattern = [0, 2, 4, 2, 0, 2, 4, 5]

        step_index = 0
        current_sample = 0

        while current_sample < num_samples:
            note_idx = arp_pattern[step_index % len(arp_pattern)]
            freq = scale[note_idx % len(scale)]
            note_duration = min(samples_per_16th, num_samples - current_sample)
            t = np.arange(note_duration) / self.SAMPLE_RATE

            # Square wave for classic arpeggiator sound
            square = np.sign(np.sin(2 * np.pi * freq * t))

            # Plucky envelope
            envelope = np.exp(-20 * t)

            arp_note = 0.08 * square * envelope

            track[current_sample:current_sample + note_duration] = arp_note

            current_sample += samples_per_16th
            step_index += 1

        return track

    # ========== PREMIUM EFFECTS ==========

    def _apply_sidechain(
        self, mix: np.ndarray, kick: np.ndarray, strength: float = 0.4
    ) -> np.ndarray:
        """Apply sidechain compression (ducking)."""
        # Create ducking envelope from kick
        kick_envelope = np.abs(kick)
        # Smooth it
        window = int(0.05 * self.SAMPLE_RATE)
        if window > 0:
            kick_envelope = np.convolve(kick_envelope, np.ones(window) / window, mode='same')

        # Create sidechain multiplier
        sidechain = 1 - strength * (kick_envelope / (np.max(kick_envelope) + 1e-6))
        sidechain = np.clip(sidechain, 0.3, 1.0)

        return mix * sidechain

    def _apply_gated_reverb(self, snare: np.ndarray, gate_time: float = 0.15) -> np.ndarray:
        """Apply gated reverb effect (classic 80s snare sound)."""
        # Simple reverb simulation
        gate_samples = int(gate_time * self.SAMPLE_RATE)

        # Find snare hits and add reverb tail
        processed = snare.copy()
        threshold = np.max(np.abs(snare)) * 0.1

        for i in range(len(snare) - gate_samples):
            if np.abs(snare[i]) > threshold:
                # Add gated reverb tail
                tail = np.exp(-10 * np.arange(gate_samples) / self.SAMPLE_RATE)
                tail *= snare[i] * 0.3
                processed[i:i + gate_samples] += tail

        return processed


class PremiumMusicGenerator:
    """
    Premium artist-influenced music generator.

    Creates structured songs with lyrics, sections, and metadata
    based on artist influences and musical characteristics.
    """

    # Artist-specific vocal characteristics
    ARTIST_VOCAL_STYLES = {
        "depeche_mode": {"gender": "male", "tone": "baritone", "energy": "medium"},
        "gary_numan": {"gender": "male", "tone": "detached", "energy": "medium"},
        "kraftwerk": {"gender": "male", "tone": "robotic", "energy": "low"},
        "new_order": {"gender": "male", "tone": "melancholic", "energy": "medium"},
        "pet_shop_boys": {"gender": "male", "tone": "smooth", "energy": "medium"},
        "human_league": {"gender": "mixed", "tone": "romantic", "energy": "medium"},
        "omd": {"gender": "male", "tone": "atmospheric", "energy": "medium"},
        "tears_for_fears": {"gender": "male", "tone": "emotive", "energy": "high"},
        "eurythmics": {"gender": "female", "tone": "powerful", "energy": "high"},
        "yazoo": {"gender": "female", "tone": "soulful", "energy": "high"},
    }

    # Mood modifiers
    MOOD_MODIFIERS = {
        "dark": {"tone_mod": "dark", "themes": ["shadows", "mystery", "depth", "intensity"]},
        "dystopian": {"tone_mod": "dystopian", "themes": ["machines", "future", "cold", "metallic"]},
        "melancholic": {"tone_mod": "melancholic", "themes": ["loss", "memory", "longing", "reflection"]},
        "romantic": {"tone_mod": "romantic", "themes": ["love", "passion", "desire", "connection"]},
        "atmospheric": {"tone_mod": "atmospheric", "themes": ["space", "dreams", "floating", "ethereal"]},
        "uplifting": {"tone_mod": "uplifting", "themes": ["hope", "rise", "light", "positive"]},
        "sophisticated": {"tone_mod": "sophisticated", "themes": ["elegance", "style", "urbane", "polished"]},
        "emotive": {"tone_mod": "emotive", "themes": ["feelings", "heart", "soul", "vulnerable"]},
        "powerful": {"tone_mod": "powerful", "themes": ["strength", "force", "bold", "commanding"]},
        "mechanical": {"tone_mod": "mechanical", "themes": ["precision", "rhythm", "systematic", "industrial"]},
    }

    def generate_song(self, request: MusicGenerateRequest) -> MusicGenerateResponse:
        """Generate a complete song blueprint from artist influences."""

        # Normalize artist names to keys
        artist_keys = []
        for artist in request.artist_influences:
            key = artist.lower().replace(" ", "_").replace("the_", "")
            if key in PremiumMusicEngine.ARTIST_DATABASE:
                artist_keys.append(key)

        # Fallback to default if no valid artists
        if not artist_keys:
            artist_keys = ["depeche_mode"]

        # Get primary artist
        primary_key = artist_keys[0]
        primary_artist = PremiumMusicEngine.ARTIST_DATABASE[primary_key]

        # Determine mood (from request or artist default)
        mood = request.mood or primary_artist["mood"]

        # Get mood modifier
        mood_mod = self.MOOD_MODIFIERS.get(mood, self.MOOD_MODIFIERS["dark"])

        # Generate track ID (deterministic from inputs)
        track_input = f"{'_'.join(request.artist_influences)}{mood}{request.reference_text or ''}"
        track_id = hashlib.md5(track_input.encode()).hexdigest()[:12]

        # Generate title
        title = self._generate_title(request.artist_influences, mood, request.reference_text)

        # Determine tempo (from request or artist average)
        if request.tempo_bpm:
            tempo_bpm = request.tempo_bpm
        else:
            tempo_ranges = [PremiumMusicEngine.ARTIST_DATABASE[k]["tempo_range"] for k in artist_keys]
            avg_min = int(np.mean([r[0] for r in tempo_ranges]))
            avg_max = int(np.mean([r[1] for r in tempo_ranges]))
            tempo_bpm = (avg_min + avg_max) // 2

        # Determine instruments
        if request.instruments:
            instruments = request.instruments
        else:
            # Merge instruments from all artists
            merged = set()
            for key in artist_keys:
                merged.update(PremiumMusicEngine.ARTIST_DATABASE[key]["instruments"])
            instruments = list(merged)

        # Determine production era
        production_era = request.production_era or primary_artist["production_era"]

        # Create vocal style
        vocal_base = self.ARTIST_VOCAL_STYLES.get(primary_key, {"gender": "male", "tone": "synthetic", "energy": "medium"})
        vocal_style = VocalStyle(
            gender=vocal_base["gender"],
            tone=f"{mood_mod['tone_mod']} {vocal_base['tone']}",
            energy=vocal_base["energy"]
        )

        # Generate hook and chorus
        hook = self._generate_hook(request.artist_influences, mood, request.reference_text)
        chorus = self._generate_chorus(request.artist_influences, mood, request.reference_text, hook)

        # Generate sections
        section_names = request.sections or ["Intro", "Verse 1", "Chorus", "Verse 2", "Bridge", "Chorus", "Outro"]
        sections = self._generate_sections(
            section_names,
            request.artist_influences,
            mood,
            request.reference_text,
            chorus
        )

        # Generate actual audio file
        audio_url = self._generate_audio(request)

        return MusicGenerateResponse(
            track_id=track_id,
            title=title,
            artist_influences=request.artist_influences,
            instruments=instruments,
            production_era=production_era,
            mood=mood,
            tempo_bpm=tempo_bpm,
            vocal_style=vocal_style,
            hook=hook,
            chorus=chorus,
            sections=sections,
            fake_audio_url=audio_url,
            saved_media_id=None
        )

    def _generate_title(self, artists: List[str], mood: str, reference_text: Optional[str]) -> str:
        """Generate a song title based on artists and mood."""
        if reference_text and len(reference_text) > 10:
            # Extract keywords from reference
            words = reference_text.split()[:4]
            return " ".join(w.capitalize() for w in words if len(w) > 3)[:40]

        # Mood-based title words
        mood_words = {
            "dark": ["Shadows", "Depths", "Mystery", "Eclipse"],
            "dystopian": ["Machines", "Future", "Metal", "Binary"],
            "melancholic": ["Memory", "Fading", "Distance", "Echoes"],
            "romantic": ["Hearts", "Touch", "Desire", "Connection"],
            "atmospheric": ["Space", "Clouds", "Dreams", "Ethereal"],
            "uplifting": ["Rising", "Light", "Hope", "Ascend"],
            "sophisticated": ["Velvet", "Elegance", "Urbane", "Style"],
            "emotive": ["Feelings", "Soul", "Tears", "Passion"],
            "powerful": ["Force", "Thunder", "Steel", "Impact"],
            "mechanical": ["Precision", "Systems", "Rhythm", "Logic"],
        }

        # Get mood word
        mood_word = mood_words.get(mood, ["Synth", "Electric", "Digital", "Wave"])[0]

        # Genre word based on synthwave/electronic
        synth_words = ["Frequency", "Pulse", "Circuit", "Voltage", "Signal"]
        synth_word = synth_words[hash(artists[0]) % len(synth_words)]

        return f"{mood_word} {synth_word}"

    def _generate_hook(self, artists: List[str], mood: str, reference_text: Optional[str]) -> str:
        """Generate a memorable hook line."""
        templates = [
            f"Lost in the {mood} frequency",
            f"Running through these {mood} nights",
            f"Feel the {mood} pulse",
            f"We're {mood} and electric",
            f"Dancing in the {mood} light",
        ]

        # Use hash to deterministically pick a template
        idx = hash(f"{'_'.join(artists)}{mood}") % len(templates)
        return templates[idx]

    def _generate_chorus(self, artists: List[str], mood: str, reference_text: Optional[str], hook: str) -> str:
        """Generate main chorus lyrics."""
        return f"""{hook}
Never looking back, we're moving forward now
Every single moment, yeah we're living loud
{hook}
This is our time, this is our sound"""

    def _generate_sections(
        self,
        section_names: List[str],
        artists: List[str],
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
                    description="Atmospheric synth intro with sequenced elements",
                    lyrics="[Instrumental with ambient synths]"
                ))

            elif "verse" in section_lower:
                verse_num = "1" if "verse 1" in section_lower or section_lower == "verse" else "2"
                sections.append(MusicSection(
                    name=section_name,
                    bars=16,
                    description=f"Verse development with electronic textures",
                    lyrics=self._generate_verse_lyrics(artists, mood, verse_num)
                ))

            elif "chorus" in section_lower:
                sections.append(MusicSection(
                    name=section_name,
                    bars=16,
                    description="Main hook section with full synth arrangement",
                    lyrics=chorus
                ))

            elif "bridge" in section_lower:
                sections.append(MusicSection(
                    name=section_name,
                    bars=8,
                    description="Synth break with arpeggiated sequences",
                    lyrics=self._generate_bridge_lyrics(artists, mood)
                ))

            elif "outro" in section_lower:
                sections.append(MusicSection(
                    name=section_name,
                    bars=8,
                    description="Gradual fade with sequenced elements",
                    lyrics="[Instrumental fade with synth echoes]"
                ))

            else:
                # Generic section
                sections.append(MusicSection(
                    name=section_name,
                    bars=12,
                    description="Musical section",
                    lyrics=self._generate_verse_lyrics(artists, mood, "1")
                ))

        return sections

    def _generate_verse_lyrics(self, artists: List[str], mood: str, verse_num: str) -> str:
        """Generate verse lyrics."""
        verse_templates = {
            "1": """In the neon glow we find our way
Through the static haze of yesterday
Synthesized emotions running through my veins
Living in this digital domain""",
            "2": """They said our world was cold and gray
But we found color in the display
Every circuit sparks with something new
This electric dream, me and you"""
        }

        return verse_templates.get(verse_num, verse_templates["1"])

    def _generate_bridge_lyrics(self, artists: List[str], mood: str) -> str:
        """Generate bridge lyrics."""
        return """And when the frequencies align
We'll transcend the space and time
Nothing can stop this signal now
We're breaking through somehow"""

    def _generate_audio(self, request: MusicGenerateRequest) -> str:
        """
        Generate premium backing track using PremiumMusicEngine.

        Args:
            request: Full music generation request with artist_influences

        Returns:
            URL path to the generated audio file
        """
        engine = PremiumMusicEngine()
        return engine.generate_backing_track(request)


class MusicService:
    """Service for premium artist-influenced music generation."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize music service."""
        self.db = db
        self.generator = PremiumMusicGenerator()

    def generate_song(self, request: MusicGenerateRequest) -> MusicGenerateResponse:
        """
        Generate a complete premium song blueprint.

        Creates structured output with lyrics, sections, and metadata
        based on artist influences.
        """
        logger.info(
            f"Generating premium song: artists={', '.join(request.artist_influences)}, "
            f"mood={request.mood or 'auto'}"
        )

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
                    "artist_influences": response.artist_influences,
                    "instruments": response.instruments,
                    "production_era": response.production_era,
                    "mood": response.mood,
                    "tempo_bpm": response.tempo_bpm,
                    "operation": "premium_song_generation",
                }
            )
            response.saved_media_id = saved_media_id

        logger.info(
            f"Generated premium song: {response.title} ({response.track_id}) - "
            f"{', '.join(response.artist_influences)}"
        )
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
