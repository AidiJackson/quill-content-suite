"""
LLM Producer Client - AI-powered refinement of producer plans.

This module provides an LLM-based "producer brain" that can refine the rule-based
producer plan with more sophisticated musical intelligence.

For now, this is a stub that makes deterministic refinements. In production,
this would connect to OpenRouter/OpenAI to use a real LLM.
"""

import os
from typing import Optional

from app.schemas.media import MusicGenerateRequest
from app.services.producer_plan_service import ProducerPlan


class LLMProducerClient:
    """
    LLM-powered producer plan refinement client.

    This client can optionally enhance the rule-based producer plan with
    AI-powered musical intelligence. If no API key is configured, it falls
    back to deterministic enhancements.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM producer client.

        Args:
            api_key: API key for LLM service (OpenRouter, OpenAI, etc.)
            model: Model identifier (e.g., "gpt-4", "claude-3-sonnet")
        """
        self.api_key = api_key
        self.model = model or "gpt-4-turbo-preview"
        self.enabled = api_key is not None

    async def refine_plan(
        self, request: MusicGenerateRequest, base_plan: ProducerPlan
    ) -> ProducerPlan:
        """
        Refine a producer plan using LLM intelligence.

        If LLM is not enabled, applies deterministic enhancements based on
        request parameters. In production, this would make an LLM API call.

        Args:
            request: Original music generation request
            base_plan: Rule-based producer plan to refine

        Returns:
            Refined ProducerPlan with enhanced musical decisions
        """
        if not self.enabled:
            # No LLM available - apply deterministic enhancements
            return self._apply_deterministic_refinements(request, base_plan)

        # TODO: Implement actual LLM API call
        # For now, use deterministic refinements even if API key is present
        return self._apply_deterministic_refinements(request, base_plan)

    def _apply_deterministic_refinements(
        self, request: MusicGenerateRequest, base_plan: ProducerPlan
    ) -> ProducerPlan:
        """
        Apply deterministic refinements to the base plan.

        This simulates what an LLM would do, making intelligent adjustments
        based on the request parameters.

        Args:
            request: Original music generation request
            base_plan: Rule-based producer plan

        Returns:
            Enhanced ProducerPlan
        """
        # Copy config for modification
        config = base_plan.config.copy()
        summary_parts = [base_plan.summary]

        text = (request.influence_text or "").lower()
        artists = [a.lower() for a in (request.influence_artists or [])]
        usage = (request.usage_context or "").lower()

        # === ENERGY & DYNAMICS REFINEMENTS ===

        # "Massive chorus" indicator
        if any(word in text for word in ["massive", "huge", "epic", "cinematic"]):
            config["energy_curve"] = "dynamic_build"
            summary_parts.append("Enhanced with dynamic build for massive impact.")

        # "Drop" or "buildup" indicators
        if any(word in text for word in ["drop", "buildup", "build up", "crescendo"]):
            if config.get("structure") and isinstance(config["structure"], list):
                # Ensure structure has a build/drop section
                if "build" not in config["structure"]:
                    config["structure"].insert(-1, "build")
                summary_parts.append("Added buildup section for tension.")

        # === TEMPO REFINEMENTS ===

        # Slow ballad indicators
        if any(word in text for word in ["ballad", "slow", "intimate", "soft"]):
            current_tempo = config.get("tempo_bpm", 100)
            config["tempo_bpm"] = min(current_tempo, 85)
            summary_parts.append("Slowed tempo for intimate feel.")

        # High energy indicators
        if any(word in text for word in ["energetic", "pumped", "hype", "intense"]):
            current_tempo = config.get("tempo_bpm", 100)
            config["tempo_bpm"] = max(current_tempo, 125)
            summary_parts.append("Increased tempo for high energy.")

        # === STRUCTURE REFINEMENTS ===

        # TikTok/Shorts optimization
        if usage in ["tiktok", "shorts"] or any(word in text for word in ["tiktok", "shorts", "viral"]):
            # Ensure hook-first structure
            config["structure"] = ["intro", "hook", "drop", "chorus"]
            config["energy_curve"] = "hook_first"
            summary_parts.append("Optimized structure for viral short-form content.")

        # Full song structure
        if usage == "full_song" or "full song" in text:
            config["structure"] = ["intro", "verse", "chorus", "verse", "bridge", "chorus", "outro"]
            config["energy_curve"] = "dynamic"
            summary_parts.append("Full song structure with bridge.")

        # === ARTIST HYBRID REFINEMENTS ===

        # Linkin Park + Eminem = nu-metal/rap-rock hybrid
        has_linkin = any("linkin park" in a for a in artists) or "linkin park" in text
        has_eminem = any("eminem" in a for a in artists) or "eminem" in text

        if has_linkin and has_eminem:
            config["artist_style"] = "linkin_park_eminem_hybrid"
            config["guitar_profile"] = "nu_metal_heavy"
            config["drum_profile"] = "hybrid_rock_hiphop"
            summary_parts.append("Created nu-metal/rap-rock hybrid sound.")

        # === MOOD & TONALITY REFINEMENTS ===

        # Dark/heavy/aggressive
        if any(word in text for word in ["heavy", "aggressive", "intense", "raw"]):
            if config.get("key", "").endswith("major"):
                # Convert to relative minor
                config["key"] = config["key"].replace("major", "minor")
            summary_parts.append("Darkened tonality for heavier feel.")

        # Uplifting/positive
        if any(word in text for word in ["uplifting", "positive", "happy", "joyful"]):
            if config.get("key", "").endswith("minor"):
                # Convert to relative major
                config["key"] = config["key"].replace("minor", "major")
            summary_parts.append("Brightened tonality for uplifting mood.")

        # === INSTRUMENTATION REFINEMENTS ===

        # Explicit guitar mentions
        if any(word in text for word in ["guitar", "guitars", "riff", "riffs"]):
            config["guitar_profile"] = "prominent_heavy"
            summary_parts.append("Guitars featured prominently.")

        # Synth/electronic mentions
        if any(word in text for word in ["synth", "electronic", "digital", "edm"]):
            config["guitar_profile"] = None  # Remove guitars
            config["synth_profile"] = "prominent_digital"
            summary_parts.append("Electronic synths featured.")

        # Drums/percussion emphasis
        if any(word in text for word in ["drums", "percussion", "beat", "groove"]):
            summary_parts.append("Emphasized drum presence.")

        # === USAGE CONTEXT REFINEMENTS ===

        if usage == "background":
            config["energy_curve"] = "steady_ambient"
            config["structure"] = ["loop", "variation", "loop"]
            summary_parts.append("Structured for background/ambient use.")

        # Build refined summary
        refined_summary = " ".join(summary_parts)

        return ProducerPlan(config=config, summary=refined_summary)


def create_llm_producer_client() -> LLMProducerClient:
    """
    Factory function to create LLM producer client from environment variables.

    Reads configuration from:
    - MUSIC_LLM_API_KEY: API key for LLM service
    - MUSIC_LLM_MODEL: Model identifier (optional)

    Returns:
        Configured LLMProducerClient instance
    """
    api_key = os.getenv("MUSIC_LLM_API_KEY")
    model = os.getenv("MUSIC_LLM_MODEL")

    return LLMProducerClient(api_key=api_key, model=model)
