"""Content generation routes."""

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.schemas.blog import (BlogGenerateRequest, BlogGenerateResponse,
                              OutlineGenerateRequest, OutlineGenerateResponse)
from app.schemas.campaign import (CampaignGenerateRequest,
                                  CampaignGenerateResponse,
                                  ContentExpandRequest, ContentExpandResponse,
                                  ContentRewriteRequest,
                                  ContentRewriteResponse,
                                  ContentShortenRequest,
                                  ContentShortenResponse)
from app.schemas.newsletter import (NewsletterGenerateRequest,
                                    NewsletterGenerateResponse)
from app.schemas.post import (HookGenerateRequest, HookGenerateResponse,
                              PostGenerateRequest, PostGenerateResponse)
from app.services.ai_client import get_ai_client
from app.services.content_service import ContentService

router = APIRouter(prefix="/content", tags=["Content Generation"])


@router.post("/blog", response_model=BlogGenerateResponse)
def generate_blog(
    request: BlogGenerateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Generate a blog post."""
    ai_client = get_ai_client()
    service = ContentService(ai_client, db)

    style_dict = request.style_profile.model_dump() if request.style_profile else None

    result = service.generate_blog(
        topic=request.topic,
        style_profile=style_dict,
        project_id=request.project_id,
    )

    return result


@router.post("/outline", response_model=OutlineGenerateResponse)
def generate_outline(
    request: OutlineGenerateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Generate a content outline."""
    ai_client = get_ai_client()
    service = ContentService(ai_client, db)

    result = service.generate_outline(
        topic=request.topic,
        sections=request.sections,
        project_id=request.project_id,
    )

    return result


@router.post("/newsletter", response_model=NewsletterGenerateResponse)
def generate_newsletter(
    request: NewsletterGenerateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Generate a newsletter."""
    ai_client = get_ai_client()
    service = ContentService(ai_client, db)

    result = service.generate_newsletter(
        subject=request.subject,
        topics=request.topics,
        tone=request.tone,
        project_id=request.project_id,
    )

    return result


@router.post("/post", response_model=PostGenerateResponse)
def generate_social_posts(
    request: PostGenerateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Generate social media posts."""
    ai_client = get_ai_client()
    service = ContentService(ai_client, db)

    platforms = [p.value for p in request.platforms]

    result = service.generate_social_posts(
        topic=request.topic,
        platforms=platforms,
        include_hooks=request.include_hooks,
        project_id=request.project_id,
    )

    return result


@router.post("/hooks", response_model=HookGenerateResponse)
def generate_hooks(
    request: HookGenerateRequest,
    current_user: CurrentUser,
):
    """Generate attention-grabbing hooks."""
    ai_client = get_ai_client()
    service = ContentService(ai_client)

    platform = request.platform.value if request.platform else None

    hooks = service.generate_hooks(
        topic=request.topic,
        count=request.count,
        platform=platform,
    )

    return {"hooks": hooks}


@router.post("/campaign", response_model=CampaignGenerateResponse)
def generate_campaign(
    request: CampaignGenerateRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Generate a content campaign."""
    ai_client = get_ai_client()
    service = ContentService(ai_client, db)

    result = service.generate_campaign(
        goal=request.goal,
        steps=request.steps,
        audience=request.audience,
        project_id=request.project_id,
    )

    return result


@router.post("/expand", response_model=ContentExpandResponse)
def expand_content(
    request: ContentExpandRequest,
    current_user: CurrentUser,
):
    """Expand content."""
    ai_client = get_ai_client()
    service = ContentService(ai_client)

    result = service.expand_content(
        text=request.text,
        target_length=request.target_length,
    )

    return result


@router.post("/shorten", response_model=ContentShortenResponse)
def shorten_content(
    request: ContentShortenRequest,
    current_user: CurrentUser,
):
    """Shorten content."""
    ai_client = get_ai_client()
    service = ContentService(ai_client)

    result = service.shorten_content(
        text=request.text,
        target_length=request.target_length,
    )

    return result


@router.post("/rewrite", response_model=ContentRewriteResponse)
def rewrite_content(
    request: ContentRewriteRequest,
    current_user: CurrentUser,
):
    """Rewrite content with instructions."""
    ai_client = get_ai_client()
    service = ContentService(ai_client)

    result = service.rewrite_content(
        text=request.text,
        instructions=request.instructions,
    )

    return result
