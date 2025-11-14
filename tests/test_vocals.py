"""Tests for vocal generation endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_generate_vocals_basic(client: TestClient):
    """Test basic vocal generation with required fields."""
    response = client.post(
        "/api/vocals/generate",
        json={
            "lyrics": "This is a test song\nWith multiple lines\nAnd some content",
            "vocal_style": {
                "gender": "male",
                "tone": "smooth",
                "energy": "medium"
            }
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "vocal_id" in data
    assert "audio_url" in data
    assert "vocal_style" in data

    # Check vocal_id is non-empty
    assert len(data["vocal_id"]) > 0

    # Check audio_url looks like a URL
    assert "http" in data["audio_url"]
    assert ".mp3" in data["audio_url"]

    # Check vocal_style is echoed back
    assert data["vocal_style"]["gender"] == "male"
    assert data["vocal_style"]["tone"] == "smooth"
    assert data["vocal_style"]["energy"] == "medium"


def test_generate_vocals_with_track_id(client: TestClient):
    """Test vocal generation with associated track ID."""
    response = client.post(
        "/api/vocals/generate",
        json={
            "track_id": "test-track-123",
            "lyrics": "Sample lyrics here",
            "vocal_style": {
                "gender": "female",
                "tone": "emotional",
                "energy": "high"
            }
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["track_id"] == "test-track-123"


def test_generate_vocals_with_tempo(client: TestClient):
    """Test vocal generation with tempo."""
    response = client.post(
        "/api/vocals/generate",
        json={
            "lyrics": "Fast tempo lyrics\nQuick and energetic",
            "vocal_style": {
                "gender": "male",
                "tone": "aggressive",
                "energy": "high"
            },
            "tempo_bpm": 150
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Duration should be calculated
    assert "duration_seconds" in data
    assert data["duration_seconds"] is not None
    assert data["duration_seconds"] > 0


def test_generate_vocals_duration_estimation(client: TestClient):
    """Test that duration is estimated reasonably."""
    # Short lyrics
    response_short = client.post(
        "/api/vocals/generate",
        json={
            "lyrics": "Short",
            "vocal_style": {
                "gender": "male",
                "tone": "smooth",
                "energy": "low"
            }
        },
        headers={"X-User-Id": "test-user"},
    )

    # Long lyrics
    long_lyrics = " ".join(["word"] * 200)  # 200 words
    response_long = client.post(
        "/api/vocals/generate",
        json={
            "lyrics": long_lyrics,
            "vocal_style": {
                "gender": "female",
                "tone": "bright",
                "energy": "medium"
            }
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response_short.status_code == 200
    assert response_long.status_code == 200

    short_duration = response_short.json()["duration_seconds"]
    long_duration = response_long.json()["duration_seconds"]

    # Longer lyrics should have longer duration
    assert long_duration > short_duration

    # Durations should be within reasonable bounds (30-240 seconds)
    assert 30 <= short_duration <= 240
    assert 30 <= long_duration <= 240


def test_generate_vocals_notes_present(client: TestClient):
    """Test that generation notes are included."""
    response = client.post(
        "/api/vocals/generate",
        json={
            "lyrics": "Test lyrics",
            "vocal_style": {
                "gender": "mixed",
                "tone": "vibrant",
                "energy": "high"
            }
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    assert "notes" in data
    assert data["notes"] is not None
    assert "Demo vocal rendering" in data["notes"]


def test_generate_vocals_missing_lyrics(client: TestClient):
    """Test that missing lyrics returns validation error."""
    response = client.post(
        "/api/vocals/generate",
        json={
            "vocal_style": {
                "gender": "male",
                "tone": "smooth",
                "energy": "medium"
            }
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 422


def test_generate_vocals_missing_vocal_style(client: TestClient):
    """Test that missing vocal_style returns validation error."""
    response = client.post(
        "/api/vocals/generate",
        json={
            "lyrics": "Test lyrics"
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 422


def test_generate_vocals_different_styles(client: TestClient):
    """Test vocal generation with different vocal styles."""
    styles = [
        {"gender": "male", "tone": "aggressive", "energy": "high"},
        {"gender": "female", "tone": "soft", "energy": "low"},
        {"gender": "mixed", "tone": "vibrant", "energy": "high"},
        {"gender": "auto", "tone": "smooth", "energy": "medium"},
    ]

    for style in styles:
        response = client.post(
            "/api/vocals/generate",
            json={
                "lyrics": "Test lyrics for different styles",
                "vocal_style": style
            },
            headers={"X-User-Id": "test-user"},
        )

        assert response.status_code == 200, f"Failed for style: {style}"
        data = response.json()

        # Audio URL should contain the gender and energy
        assert style["gender"] in data["audio_url"]
        assert style["energy"] in data["audio_url"]


def test_generate_vocals_with_reference_text(client: TestClient):
    """Test vocal generation with reference text."""
    response = client.post(
        "/api/vocals/generate",
        json={
            "lyrics": "Sample lyrics",
            "vocal_style": {
                "gender": "female",
                "tone": "dreamy",
                "energy": "low"
            },
            "reference_text": "Think Billie Eilish style vocals"
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    assert "vocal_id" in data
    assert "audio_url" in data
