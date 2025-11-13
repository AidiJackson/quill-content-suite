"""Time utilities."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC time with timezone info."""
    return datetime.now(timezone.utc)


def to_timestamp(dt: datetime) -> int:
    """Convert datetime to Unix timestamp."""
    return int(dt.timestamp())


def from_timestamp(ts: int) -> datetime:
    """Convert Unix timestamp to datetime."""
    return datetime.fromtimestamp(ts, tz=timezone.utc)
