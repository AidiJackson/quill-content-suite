"""Content project management service."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.content_item import ContentItem
from app.models.content_project import ContentProject
from app.models.media_file import MediaFile
from app.schemas.project import ContentProjectCreate, ContentProjectUpdate

logger = get_logger(__name__)


class ProjectService:
    """Service for managing content projects."""

    def __init__(self, db: Session):
        """Initialize project service."""
        self.db = db

    def create_project(self, project_data: ContentProjectCreate) -> ContentProject:
        """Create a new content project."""
        logger.info(f"Creating project: {project_data.title}")

        project = ContentProject(
            user_id=project_data.user_id,
            title=project_data.title,
            description=project_data.description,
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        logger.info(f"Created project: {project.id}")
        return project

    def get_project(self, project_id: str) -> Optional[ContentProject]:
        """Get a project by ID."""
        return (
            self.db.query(ContentProject)
            .filter(ContentProject.id == project_id)
            .first()
        )

    def list_projects(
        self, user_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[ContentProject]:
        """List projects, optionally filtered by user."""
        query = self.db.query(ContentProject)

        if user_id:
            query = query.filter(ContentProject.user_id == user_id)

        return query.offset(skip).limit(limit).all()

    def update_project(
        self, project_id: str, project_data: ContentProjectUpdate
    ) -> Optional[ContentProject]:
        """Update a project."""
        project = self.get_project(project_id)

        if not project:
            return None

        update_data = project_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(project, field, value)

        self.db.commit()
        self.db.refresh(project)

        logger.info(f"Updated project: {project.id}")
        return project

    def delete_project(self, project_id: str) -> bool:
        """Delete a project."""
        project = self.get_project(project_id)

        if not project:
            return False

        self.db.delete(project)
        self.db.commit()

        logger.info(f"Deleted project: {project_id}")
        return True

    def get_project_content(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[ContentItem]:
        """Get all content items for a project."""
        return (
            self.db.query(ContentItem)
            .filter(ContentItem.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_project_media(
        self, project_id: str, skip: int = 0, limit: int = 100
    ) -> List[MediaFile]:
        """Get all media files for a project."""
        return (
            self.db.query(MediaFile)
            .filter(MediaFile.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_content_item(self, item_id: str) -> Optional[ContentItem]:
        """Get a content item by ID."""
        return self.db.query(ContentItem).filter(ContentItem.id == item_id).first()

    def delete_content_item(self, item_id: str) -> bool:
        """Delete a content item."""
        item = self.get_content_item(item_id)

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()

        logger.info(f"Deleted content item: {item_id}")
        return True

    def get_media_file(self, media_id: str) -> Optional[MediaFile]:
        """Get a media file by ID."""
        return self.db.query(MediaFile).filter(MediaFile.id == media_id).first()

    def delete_media_file(self, media_id: str) -> bool:
        """Delete a media file."""
        media = self.get_media_file(media_id)

        if not media:
            return False

        self.db.delete(media)
        self.db.commit()

        logger.info(f"Deleted media file: {media_id}")
        return True
