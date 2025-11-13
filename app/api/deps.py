"""API dependencies for database and authentication."""

from typing import Annotated, Generator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db

settings = get_settings()


def get_current_user(
    x_user_id: Annotated[str, Header()] = "default-user",
) -> str:
    """
    Get current user from header.

    For MVP, this is a simple header-based auth.
    In production, this would validate JWT tokens.
    """
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID header is required",
        )

    return x_user_id


def verify_api_key(
    x_api_key: Annotated[str | None, Header()] = None,
) -> bool:
    """
    Verify API key if enabled.

    For MVP, this is optional and can be disabled in config.
    """
    if not settings.api_key_enabled:
        return True

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return True


# Type aliases for common dependencies
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[str, Depends(get_current_user)]
APIKeyVerified = Annotated[bool, Depends(verify_api_key)]
