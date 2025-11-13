"""AI client service with Fake and OpenAI implementations."""

import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class AIClient(ABC):
    """Abstract base class for AI clients."""

    @abstractmethod
    def generate_blog(
        self, topic: str, style_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a blog post."""
        pass

    @abstractmethod
    def generate_newsletter(
        self, subject: str, topics: List[str], tone: str = "professional"
    ) -> Dict[str, Any]:
        """Generate a newsletter."""
        pass

    @abstractmethod
    def generate_social_posts(
        self, topic: str, platforms: List[str], include_hooks: bool = True
    ) -> List[Dict[str, Any]]:
        """Generate social media posts."""
        pass

    @abstractmethod
    def generate_campaign(
        self, goal: str, steps: int, audience: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a campaign."""
        pass

    @abstractmethod
    def expand(self, text: str, target_length: str = "double") -> str:
        """Expand text."""
        pass

    @abstractmethod
    def shorten(self, text: str, target_length: Optional[int] = None) -> str:
        """Shorten text."""
        pass

    @abstractmethod
    def rewrite(self, text: str, instructions: str) -> str:
        """Rewrite text with instructions."""
        pass

    @abstractmethod
    def virality_score(self, text: str) -> Dict[str, Any]:
        """Calculate virality score."""
        pass

    @abstractmethod
    def generate_outline(self, topic: str, sections: int = 5) -> List[str]:
        """Generate content outline."""
        pass

    @abstractmethod
    def generate_hooks(
        self, topic: str, count: int = 5, platform: Optional[str] = None
    ) -> List[str]:
        """Generate attention-grabbing hooks."""
        pass


class FakeAIClient(AIClient):
    """Fake AI client for deterministic testing and development."""

    def generate_blog(
        self, topic: str, style_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a fake blog post."""
        return {
            "title": f"The Ultimate Guide to {topic}",
            "content": f"""# The Ultimate Guide to {topic}

Introduction to {topic} and why it matters in today's world.

## Section 1: Understanding {topic}
This section explores the fundamentals of {topic} and provides context.

## Section 2: Best Practices
Here are the key best practices for {topic}:
- Practice 1: Focus on quality
- Practice 2: Stay consistent
- Practice 3: Measure results

## Section 3: Common Challenges
When working with {topic}, you may encounter these challenges.

## Conclusion
{topic} is essential for success in the modern era. By following these guidelines,
you'll be well on your way to mastery.""",
            "word_count": 120,
            "metadata": {
                "style": style_profile or {},
                "generated_by": "FakeAI",
            },
        }

    def generate_newsletter(
        self, subject: str, topics: List[str], tone: str = "professional"
    ) -> Dict[str, Any]:
        """Generate a fake newsletter."""
        sections = [
            {"heading": f"Deep Dive: {topic}", "content": f"Analysis of {topic}..."}
            for topic in topics[:3]
        ]

        return {
            "subject": subject,
            "preview_text": f"This week's insights on {', '.join(topics[:2])}",
            "sections": sections,
            "cta": "Read more on our blog",
            "word_count": len(topics) * 50,
        }

    def generate_social_posts(
        self, topic: str, platforms: List[str], include_hooks: bool = True
    ) -> List[Dict[str, Any]]:
        """Generate fake social media posts."""
        posts = []

        post_templates = {
            "linkedin": "🔥 Hot take on {topic}:\n\nKey insights that will transform your approach.\n\n#professional #growth",
            "twitter": "🧵 Thread on {topic}:\n\n1/ Here's what you need to know\n2/ The game-changing insight\n3/ How to apply this today",
            "facebook": "Let's talk about {topic}!\n\nI've learned so much about this recently...\n\nWhat's your experience?",
            "reddit": "[Serious] Discussion: {topic}\n\nI wanted to share some thoughts on this topic...",
            "instagram": "✨ {topic} ✨\n\nSwipe to learn more 👉\n\n#content #inspiration",
        }

        for platform in platforms:
            template = post_templates.get(platform, "Check out my thoughts on {topic}!")
            content = template.format(topic=topic)

            posts.append(
                {
                    "platform": platform,
                    "content": content,
                    "character_count": len(content),
                    "hashtags": [
                        "content",
                        "marketing",
                        topic.replace(" ", "").lower(),
                    ],
                }
            )

        return posts

    def generate_campaign(
        self, goal: str, steps: int, audience: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a fake campaign."""
        campaign_steps = []

        for i in range(steps):
            campaign_steps.append(
                {
                    "step_number": i + 1,
                    "subject": f"Step {i + 1}: Moving towards {goal}",
                    "content": f"This is step {i + 1} in your journey to {goal}...",
                    "delay_days": i * 3,
                }
            )

        return {
            "goal": goal,
            "audience": audience,
            "steps": campaign_steps,
            "total_duration_days": (steps - 1) * 3,
        }

    def expand(self, text: str, target_length: str = "double") -> str:
        """Expand text (fake implementation)."""
        expansion = f"{text}\n\nFurthermore, it's important to note that this concept extends beyond the surface level. "
        expansion += (
            f"The implications are far-reaching and deserve careful consideration. "
        )
        expansion += f"By examining this from multiple angles, we gain deeper insights."
        return expansion

    def shorten(self, text: str, target_length: Optional[int] = None) -> str:
        """Shorten text (fake implementation)."""
        words = text.split()
        target = target_length or len(words) // 2
        return " ".join(words[:target]) + "..."

    def rewrite(self, text: str, instructions: str) -> str:
        """Rewrite text (fake implementation)."""
        return f"[Rewritten with: {instructions}]\n\n{text}"

    def virality_score(self, text: str) -> Dict[str, Any]:
        """Calculate fake virality score."""
        # Deterministic scoring based on text length and content
        base_score = min(len(text) // 10, 100)
        hook_score = min(base_score + 10, 100)
        structure_score = min(base_score + 5, 100)
        niche_score = min(base_score, 100)

        return {
            "hook_score": hook_score,
            "structure_score": structure_score,
            "niche_score": niche_score,
            "overall_score": (hook_score + structure_score + niche_score) // 3,
            "predicted_engagement": round((hook_score / 100) * 1000, 2),
            "recommendations": [
                "Add more emotional triggers",
                "Include a clear call-to-action",
                "Use more specific examples",
            ],
        }

    def generate_outline(self, topic: str, sections: int = 5) -> List[str]:
        """Generate fake outline."""
        outline = [f"Introduction to {topic}"]

        for i in range(1, sections - 1):
            outline.append(f"Section {i}: Key Aspect of {topic}")

        outline.append(f"Conclusion: The Future of {topic}")

        return outline

    def generate_hooks(
        self, topic: str, count: int = 5, platform: Optional[str] = None
    ) -> List[str]:
        """Generate fake hooks."""
        hooks = [
            f"🔥 You won't believe this about {topic}",
            f"The {topic} secret nobody talks about",
            f"Stop doing {topic} wrong (here's how)",
            f"I spent 100 hours learning {topic}. Here's what I discovered:",
            f"The surprising truth about {topic}",
            f"Why {topic} is about to change everything",
            f"Here's what everyone gets wrong about {topic}",
            f"The {topic} strategy that 10x'd my results",
        ]

        return hooks[:count]


class OpenAIAIClient(AIClient):
    """OpenAI-based AI client (stub for MVP)."""

    def __init__(self):
        """Initialize OpenAI client."""
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured, falling back to Fake client")
            self._fallback = FakeAIClient()
        else:
            # In a real implementation, initialize OpenAI client here
            # from openai import OpenAI
            # self.client = OpenAI(api_key=settings.openai_api_key)
            self._fallback = FakeAIClient()
            logger.info("OpenAI client initialized (using fallback for MVP)")

    def generate_blog(
        self, topic: str, style_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate blog using OpenAI (currently falls back to Fake)."""
        return self._fallback.generate_blog(topic, style_profile)

    def generate_newsletter(
        self, subject: str, topics: List[str], tone: str = "professional"
    ) -> Dict[str, Any]:
        """Generate newsletter using OpenAI (currently falls back to Fake)."""
        return self._fallback.generate_newsletter(subject, topics, tone)

    def generate_social_posts(
        self, topic: str, platforms: List[str], include_hooks: bool = True
    ) -> List[Dict[str, Any]]:
        """Generate posts using OpenAI (currently falls back to Fake)."""
        return self._fallback.generate_social_posts(topic, platforms, include_hooks)

    def generate_campaign(
        self, goal: str, steps: int, audience: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate campaign using OpenAI (currently falls back to Fake)."""
        return self._fallback.generate_campaign(goal, steps, audience)

    def expand(self, text: str, target_length: str = "double") -> str:
        """Expand text using OpenAI (currently falls back to Fake)."""
        return self._fallback.expand(text, target_length)

    def shorten(self, text: str, target_length: Optional[int] = None) -> str:
        """Shorten text using OpenAI (currently falls back to Fake)."""
        return self._fallback.shorten(text, target_length)

    def rewrite(self, text: str, instructions: str) -> str:
        """Rewrite text using OpenAI (currently falls back to Fake)."""
        return self._fallback.rewrite(text, instructions)

    def virality_score(self, text: str) -> Dict[str, Any]:
        """Score virality using OpenAI (currently falls back to Fake)."""
        return self._fallback.virality_score(text)

    def generate_outline(self, topic: str, sections: int = 5) -> List[str]:
        """Generate outline using OpenAI (currently falls back to Fake)."""
        return self._fallback.generate_outline(topic, sections)

    def generate_hooks(
        self, topic: str, count: int = 5, platform: Optional[str] = None
    ) -> List[str]:
        """Generate hooks using OpenAI (currently falls back to Fake)."""
        return self._fallback.generate_hooks(topic, count, platform)


def get_ai_client() -> AIClient:
    """Get AI client instance based on configuration."""
    if settings.use_fake_ai:
        return FakeAIClient()
    else:
        return OpenAIAIClient()
