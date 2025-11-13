"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import audio, content, health, projects, video, virality
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.db.init_db import init_db

# Setup logging
setup_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting up Quillography Content Suite...")

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

    yield

    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered content creation, editing, campaign, and media processing service",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(content.router)
app.include_router(virality.router)
app.include_router(video.router)
app.include_router(audio.router)

logger.info(f"{settings.app_name} initialized successfully")
