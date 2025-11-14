"""Dashboard summary routes."""

from datetime import datetime, timedelta

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import func

from app.api.deps import CurrentUser, DBSession
from app.models.content_item import ContentItem
from app.models.content_project import ContentProject
from app.models.media_file import MediaFile, MediaType
from app.models.virality_score import ViralityScore

router = APIRouter(prefix="", tags=["Dashboard"])


class DashboardSummaryResponse(BaseModel):
    """Dashboard summary statistics."""

    active_projects: int
    items_created_this_week: int
    avg_virality_score: float
    video_clips_generated: int
    tracks_in_production: int


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Get dashboard summary statistics for the current user.

    Returns:
        - active_projects: Total number of projects
        - items_created_this_week: Content items created in the last 7 days
        - avg_virality_score: Average overall virality score
        - video_clips_generated: Total video media files
        - tracks_in_production: Total audio media files
    """
    # Calculate date one week ago
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    # Active projects count
    active_projects = (
        db.query(func.count(ContentProject.id))
        .filter(ContentProject.user_id == current_user)
        .scalar()
        or 0
    )

    # Content items created this week
    items_created_this_week = (
        db.query(func.count(ContentItem.id))
        .join(ContentProject)
        .filter(
            ContentProject.user_id == current_user,
            ContentItem.created_at >= one_week_ago,
        )
        .scalar()
        or 0
    )

    # Average virality score
    # Calculate the average of (hook_score + structure_score + niche_score) / 3
    avg_scores = (
        db.query(
            func.avg(
                (
                    ViralityScore.hook_score
                    + ViralityScore.structure_score
                    + ViralityScore.niche_score
                )
                / 3.0
            )
        )
        .join(ContentItem)
        .join(ContentProject)
        .filter(ContentProject.user_id == current_user)
        .scalar()
    )
    avg_virality_score = round(float(avg_scores), 1) if avg_scores else 0.0

    # Video clips count
    video_clips_generated = (
        db.query(func.count(MediaFile.id))
        .join(ContentProject)
        .filter(
            ContentProject.user_id == current_user,
            MediaFile.type == MediaType.VIDEO,
        )
        .scalar()
        or 0
    )

    # Audio tracks count
    tracks_in_production = (
        db.query(func.count(MediaFile.id))
        .join(ContentProject)
        .filter(
            ContentProject.user_id == current_user,
            MediaFile.type == MediaType.AUDIO,
        )
        .scalar()
        or 0
    )

    return DashboardSummaryResponse(
        active_projects=active_projects,
        items_created_this_week=items_created_this_week,
        avg_virality_score=avg_virality_score,
        video_clips_generated=video_clips_generated,
        tracks_in_production=tracks_in_production,
    )
