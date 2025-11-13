"""ID generation utilities."""

from uuid import uuid4


def generate_id() -> str:
    """Generate a unique ID string."""
    return str(uuid4())


def generate_short_id() -> str:
    """Generate a short unique ID (first 8 characters of UUID)."""
    return str(uuid4())[:8]
