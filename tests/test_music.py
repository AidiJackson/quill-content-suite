"""Tests for music generation endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_generate_music_basic(client: TestClient):
    """Test basic music generation with required fields."""
    response = client.post(
        "/api/music/generate",
        json={
            "genre": "trap",
            "mood": "dark",
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "track_id" in data
    assert "title" in data
    assert "genre" in data
    assert "mood" in data
    assert "vocal_style" in data
    assert "hook" in data
    assert "chorus" in data
    assert "sections" in data
    assert "fake_audio_url" in data

    # Check title is non-empty
    assert len(data["title"]) > 0

    # Check at least 3 sections
    assert len(data["sections"]) >= 3

    # Check vocal style structure
    vocal = data["vocal_style"]
    assert "gender" in vocal
    assert "tone" in vocal
    assert "energy" in vocal

    # Check fake_audio_url format
    assert data["fake_audio_url"].startswith("https://")
    assert ".mp3" in data["fake_audio_url"]


def test_generate_music_with_tempo(client: TestClient):
    """Test music generation with custom tempo."""
    response = client.post(
        "/api/music/generate",
        json={
            "genre": "edm",
            "mood": "energetic",
            "tempo_bpm": 128,
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["tempo_bpm"] == 128


def test_generate_music_with_reference(client: TestClient):
    """Test music generation with reference text."""
    response = client.post(
        "/api/music/generate",
        json={
            "genre": "lofi",
            "mood": "chill",
            "reference_text": "Something like chilled night drive",
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Title should incorporate reference text
    assert len(data["title"]) > 0


def test_generate_music_with_custom_sections(client: TestClient):
    """Test music generation with custom sections."""
    custom_sections = ["Intro", "Verse", "Chorus", "Outro"]

    response = client.post(
        "/api/music/generate",
        json={
            "genre": "rnb",
            "mood": "emotional",
            "sections": custom_sections,
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Should have the requested number of sections
    assert len(data["sections"]) == len(custom_sections)

    # Check section structure
    for section in data["sections"]:
        assert "name" in section
        assert "bars" in section
        assert "description" in section
        assert "lyrics" in section
        assert section["bars"] > 0


def test_generate_music_various_genres(client: TestClient):
    """Test music generation with different genres."""
    genres = ["trap", "drill", "afrobeat", "lofi", "pop", "edm", "rnb", "hiphop"]

    for genre in genres:
        response = client.post(
            "/api/music/generate",
            json={
                "genre": genre,
                "mood": "energetic",
            },
            headers={"X-User-Id": "test-user"},
        )

        assert response.status_code == 200, f"Failed for genre: {genre}"
        data = response.json()
        assert data["genre"] == genre


def test_generate_music_missing_required_fields(client: TestClient):
    """Test music generation with missing required fields."""
    # Missing genre
    response = client.post(
        "/api/music/generate",
        json={
            "mood": "dark",
        },
        headers={"X-User-Id": "test-user"},
    )
    assert response.status_code == 422

    # Missing mood
    response = client.post(
        "/api/music/generate",
        json={
            "genre": "trap",
        },
        headers={"X-User-Id": "test-user"},
    )
    assert response.status_code == 422


def test_generate_music_deterministic(client: TestClient):
    """Test that the same inputs produce the same output."""
    request_data = {
        "genre": "pop",
        "mood": "uplifting",
        "tempo_bpm": 120,
    }

    # Make two requests with identical data
    response1 = client.post(
        "/api/music/generate",
        json=request_data,
        headers={"X-User-Id": "test-user"},
    )
    response2 = client.post(
        "/api/music/generate",
        json=request_data,
        headers={"X-User-Id": "test-user"},
    )

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    # Track IDs should be the same (deterministic)
    assert data1["track_id"] == data2["track_id"]
    assert data1["title"] == data2["title"]
    assert data1["hook"] == data2["hook"]
