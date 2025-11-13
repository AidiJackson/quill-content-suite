"""Content project routes."""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DBSession
from app.schemas.content_item import ContentItemResponse
from app.schemas.media import MediaFileResponse
from app.schemas.project import (ContentProjectCreate, ContentProjectResponse,
                                 ContentProjectUpdate)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "", response_model=ContentProjectResponse, status_code=status.HTTP_201_CREATED
)
def create_project(
    project_data: ContentProjectCreate,
    db: DBSession,
    current_user: CurrentUser,
):
    """Create a new content project."""
    service = ProjectService(db)
    project = service.create_project(project_data)
    return project


@router.get("", response_model=List[ContentProjectResponse])
def list_projects(
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """List all projects for the current user."""
    service = ProjectService(db)
    projects = service.list_projects(user_id=current_user, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=ContentProjectResponse)
def get_project(
    project_id: str,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get a specific project."""
    service = ProjectService(db)
    project = service.get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.patch("/{project_id}", response_model=ContentProjectResponse)
def update_project(
    project_id: str,
    project_data: ContentProjectUpdate,
    db: DBSession,
    current_user: CurrentUser,
):
    """Update a project."""
    service = ProjectService(db)
    project = service.update_project(project_id, project_data)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    db: DBSession,
    current_user: CurrentUser,
):
    """Delete a project."""
    service = ProjectService(db)
    deleted = service.delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return None


@router.get("/{project_id}/content", response_model=List[ContentItemResponse])
def list_project_content(
    project_id: str,
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """List all content items for a project."""
    service = ProjectService(db)

    # Verify project exists
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    content_items = service.get_project_content(project_id, skip=skip, limit=limit)
    return content_items


@router.get("/{project_id}/media", response_model=List[MediaFileResponse])
def list_project_media(
    project_id: str,
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """List all media files for a project."""
    service = ProjectService(db)

    # Verify project exists
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    media_files = service.get_project_media(project_id, skip=skip, limit=limit)
    return media_files
