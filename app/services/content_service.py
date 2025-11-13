"""Content generation service."""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.content_item import ContentItem, ContentType
from app.services.ai_client import AIClient

logger = get_logger(__name__)


class ContentService:
    """Service for generating and managing content."""

    def __init__(self, ai_client: AIClient, db: Optional[Session] = None):
        """Initialize content service."""
        self.ai_client = ai_client
        self.db = db

    def generate_blog(
        self,
        topic: str,
        style_profile: Optional[Dict[str, Any]] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a blog post."""
        logger.info(f"Generating blog for topic: {topic}")

        result = self.ai_client.generate_blog(topic, style_profile)

        saved_item_id = None
        if project_id and self.db:
            saved_item_id = self._save_content_item(
                project_id=project_id,
                content_type=ContentType.BLOG,
                title=result["title"],
                content=result["content"],
                meta=result.get("metadata", {}),
            )

        return {
            **result,
            "saved_item_id": saved_item_id,
        }

    def generate_outline(
        self, topic: str, sections: int = 5, project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate content outline."""
        logger.info(f"Generating outline for topic: {topic}")

        outline_sections = self.ai_client.generate_outline(topic, sections)

        saved_item_id = None
        if project_id and self.db:
            content = "\n".join(
                f"{i + 1}. {section}" for i, section in enumerate(outline_sections)
            )
            saved_item_id = self._save_content_item(
                project_id=project_id,
                content_type=ContentType.OUTLINE,
                title=f"Outline: {topic}",
                content=content,
                meta={"sections": sections},
            )

        return {
            "topic": topic,
            "sections": outline_sections,
            "saved_item_id": saved_item_id,
        }

    def generate_newsletter(
        self,
        subject: str,
        topics: List[str],
        tone: str = "professional",
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a newsletter."""
        logger.info(f"Generating newsletter: {subject}")

        result = self.ai_client.generate_newsletter(subject, topics, tone)

        saved_item_id = None
        if project_id and self.db:
            # Convert newsletter to text format
            content = f"# {result['subject']}\n\n"
            content += f"{result['preview_text']}\n\n"

            for section in result["sections"]:
                content += f"## {section['heading']}\n{section['content']}\n\n"

            content += f"\n---\n{result['cta']}"

            saved_item_id = self._save_content_item(
                project_id=project_id,
                content_type=ContentType.NEWSLETTER,
                title=result["subject"],
                content=content,
                meta={"tone": tone, "topics": topics},
            )

        return {
            **result,
            "saved_item_id": saved_item_id,
        }

    def generate_social_posts(
        self,
        topic: str,
        platforms: List[str],
        include_hooks: bool = True,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate social media posts."""
        logger.info(f"Generating social posts for topic: {topic}")

        posts = self.ai_client.generate_social_posts(topic, platforms, include_hooks)

        saved_item_ids = []
        if project_id and self.db:
            for post in posts:
                saved_id = self._save_content_item(
                    project_id=project_id,
                    content_type=ContentType.POST,
                    title=f"{post['platform'].title()} post: {topic}",
                    content=post["content"],
                    meta={
                        "platform": post["platform"],
                        "character_count": post["character_count"],
                        "hashtags": post["hashtags"],
                    },
                )
                saved_item_ids.append(saved_id)

        return {
            "posts": posts,
            "saved_item_ids": saved_item_ids if saved_item_ids else None,
        }

    def generate_hooks(
        self, topic: str, count: int = 5, platform: Optional[str] = None
    ) -> List[str]:
        """Generate attention-grabbing hooks."""
        logger.info(f"Generating {count} hooks for topic: {topic}")
        return self.ai_client.generate_hooks(topic, count, platform)

    def generate_campaign(
        self,
        goal: str,
        steps: int = 3,
        audience: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a campaign."""
        logger.info(f"Generating campaign for goal: {goal}")

        result = self.ai_client.generate_campaign(goal, steps, audience)

        saved_item_id = None
        if project_id and self.db:
            # Convert campaign to text format
            content = f"# Campaign: {goal}\n\n"
            if audience:
                content += f"**Audience:** {audience}\n\n"

            content += f"**Duration:** {result['total_duration_days']} days\n\n"

            for step in result["steps"]:
                content += f"## Step {step['step_number']}: {step['subject']}\n"
                content += f"**Delay:** {step['delay_days']} days\n\n"
                content += f"{step['content']}\n\n"

            saved_item_id = self._save_content_item(
                project_id=project_id,
                content_type=ContentType.CAMPAIGN,
                title=f"Campaign: {goal}",
                content=content,
                meta={"steps": steps, "audience": audience},
            )

        return {
            **result,
            "saved_item_id": saved_item_id,
        }

    def expand_content(
        self, text: str, target_length: str = "double"
    ) -> Dict[str, Any]:
        """Expand content."""
        logger.info("Expanding content")
        expanded = self.ai_client.expand(text, target_length)

        return {
            "original_length": len(text),
            "expanded_length": len(expanded),
            "content": expanded,
        }

    def shorten_content(
        self, text: str, target_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """Shorten content."""
        logger.info("Shortening content")
        shortened = self.ai_client.shorten(text, target_length)

        return {
            "original_length": len(text),
            "shortened_length": len(shortened),
            "content": shortened,
        }

    def rewrite_content(self, text: str, instructions: str) -> Dict[str, Any]:
        """Rewrite content with instructions."""
        logger.info(f"Rewriting content with instructions: {instructions}")
        rewritten = self.ai_client.rewrite(text, instructions)

        return {
            "original": text,
            "rewritten": rewritten,
        }

    def _save_content_item(
        self,
        project_id: str,
        content_type: ContentType,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Save content item to database."""
        if not self.db:
            raise ValueError("Database session required to save content")

        item = ContentItem(
            project_id=project_id,
            type=content_type,
            title=title,
            content=content,
            meta=metadata,
        )

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        logger.info(f"Saved content item: {item.id}")
        return item.id
