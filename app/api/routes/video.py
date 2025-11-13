"""Video processing routes."""

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.schemas.media import (VideoCaptionsRequest, VideoCaptionsResponse,
                               VideoResizeRequest, VideoResizeResponse,
                               VideoShortsRequest, VideoShortsResponse,
                               VideoTrimRequest, VideoTrimResponse)
from app.services.video_service import VideoService

router = APIRouter(prefix="/video", tags=["Video Processing"])


@router.post("/trim", response_model=VideoTrimResponse)
def trim_video(
    request: VideoTrimRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Trim a video."""
    service = VideoService(db)

    result = service.trim_video(
        input_url=request.input_url,
        start_time=request.start_time,
        end_time=request.end_time,
        project_id=request.project_id,
    )

    return result


@router.post("/captions", response_model=VideoCaptionsResponse)
def generate_captions(
    request: VideoCaptionsRequest,
    current_user: CurrentUser,
):
    """Generate captions for a video."""
    service = VideoService()

    result = service.generate_captions(input_url=request.input_url)

    return result


@router.post("/resize", response_model=VideoResizeResponse)
def resize_video(
    request: VideoResizeRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Resize video to target aspect ratio."""
    service = VideoService(db)

    result = service.resize_video(
        input_url=request.input_url,
        aspect_ratio=request.aspect_ratio,
        project_id=request.project_id,
    )

    return result


@router.post("/shorts", response_model=VideoShortsResponse)
def generate_shorts(
    request: VideoShortsRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """Generate short clips from a video."""
    service = VideoService(db)

    result = service.generate_shorts(
        input_url=request.input_url,
        count=request.count,
        project_id=request.project_id,
    )

    return result
