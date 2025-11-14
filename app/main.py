"""Main FastAPI application."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import audio, content, health, music, projects, summary, video, virality, vocals
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

# Include API routers under /api prefix
app.include_router(health.router, prefix="/api")
app.include_router(summary.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(content.router, prefix="/api")
app.include_router(virality.router, prefix="/api")
app.include_router(video.router, prefix="/api")
app.include_router(audio.router, prefix="/api")
app.include_router(music.router, prefix="/api")
app.include_router(vocals.router, prefix="/api")

# Serve frontend static files in production
frontend_build_path = Path(__file__).parent.parent / "frontend" / "build"
if frontend_build_path.exists():
    logger.info(f"Serving frontend from {frontend_build_path}")
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=str(frontend_build_path / "assets")), name="assets")
    
    # Serve index.html for all other routes (SPA fallback)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the React frontend for all non-API routes."""
        # If requesting a specific file that exists, serve it
        file_path = frontend_build_path / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # Otherwise serve index.html for client-side routing
        return FileResponse(frontend_build_path / "index.html")
else:
    logger.warning(f"Frontend build not found at {frontend_build_path}. Run 'npm run build' in the frontend directory.")

logger.info(f"{settings.app_name} initialized successfully")
