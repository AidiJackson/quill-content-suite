"""Tests for music generation endpoints."""

import os
import pytest
from fastapi.testclient import TestClient
from pathlib import Path


def test_generate_music_basic(client: TestClient):
    """Test basic premium music generation with artist influences."""
    response = client.post(
        "/api/music/generate",
        json={
            "artist_influences": ["Depeche Mode"],
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "track_id" in data
    assert "title" in data
    assert "artist_influences" in data
    assert "instruments" in data
    assert "production_era" in data
    assert "mood" in data
    assert "tempo_bpm" in data
    assert "vocal_style" in data
    assert "hook" in data
    assert "chorus" in data
    assert "sections" in data
    assert "fake_audio_url" in data

    # Check title is non-empty
    assert len(data["title"]) > 0

    # Check artist influences
    assert data["artist_influences"] == ["Depeche Mode"]
    assert isinstance(data["instruments"], list)
    assert len(data["instruments"]) > 0

    # Check at least 3 sections
    assert len(data["sections"]) >= 3

    # Check vocal style structure
    vocal = data["vocal_style"]
    assert "gender" in vocal
    assert "tone" in vocal
    assert "energy" in vocal

    # Check fake_audio_url format (now points to static file)
    assert data["fake_audio_url"].startswith("/static/audio/music/")
    assert ".wav" in data["fake_audio_url"]


def test_generate_music_with_tempo(client: TestClient):
    """Test premium music generation with custom tempo."""
    response = client.post(
        "/api/music/generate",
        json={
            "artist_influences": ["Pet Shop Boys"],
            "mood": "sophisticated",
            "tempo_bpm": 125,
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["tempo_bpm"] == 125
    assert "Pet Shop Boys" in data["artist_influences"]


def test_generate_music_with_reference(client: TestClient):
    """Test premium music generation with reference text."""
    response = client.post(
        "/api/music/generate",
        json={
            "artist_influences": ["Gary Numan"],
            "mood": "dystopian",
            "reference_text": "Something like a dystopian future cityscape",
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Title should incorporate reference text
    assert len(data["title"]) > 0
    assert "Gary Numan" in data["artist_influences"]


def test_generate_music_with_custom_sections(client: TestClient):
    """Test premium music generation with custom sections."""
    custom_sections = ["Intro", "Verse", "Chorus", "Outro"]

    response = client.post(
        "/api/music/generate",
        json={
            "artist_influences": ["Tears for Fears"],
            "mood": "emotive",
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


def test_generate_music_multiple_artists(client: TestClient):
    """Test premium music generation with multiple artist influences."""
    artists = ["Depeche Mode", "Gary Numan", "New Order"]

    response = client.post(
        "/api/music/generate",
        json={
            "artist_influences": artists,
            "mood": "dark",
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Check all artists are present
    for artist in artists:
        assert artist in data["artist_influences"]


def test_generate_music_missing_required_fields(client: TestClient):
    """Test music generation with missing required fields."""
    # Missing artist_influences
    response = client.post(
        "/api/music/generate",
        json={
            "mood": "dark",
        },
        headers={"X-User-Id": "test-user"},
    )
    assert response.status_code == 422


def test_generate_music_deterministic(client: TestClient):
    """Test that the same inputs produce the same output."""
    request_data = {
        "artist_influences": ["Kraftwerk"],
        "mood": "mechanical",
        "tempo_bpm": 125,
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


def test_procedural_audio_file_created(client: TestClient):
    """Test that premium procedural audio files are actually created on disk."""
    response = client.post(
        "/api/music/generate",
        json={
            "artist_influences": ["Depeche Mode"],
            "mood": "dark",
            "tempo_bpm": 120,
        },
        headers={"X-User-Id": "test-user"},
    )

    assert response.status_code == 200
    data = response.json()

    # Extract filename from URL
    audio_url = data["fake_audio_url"]
    assert audio_url.startswith("/static/audio/music/")

    # Construct file path
    filename = audio_url.split("/")[-1]
    static_dir = Path(__file__).parent.parent / "static" / "audio" / "music"
    file_path = static_dir / filename

    # Check file exists
    assert file_path.exists(), f"Audio file not found at {file_path}"

    # Check file size is reasonable (should be > 0)
    file_size = file_path.stat().st_size
    assert file_size > 0, "Audio file is empty"

    # For an 8-bar track at 120 BPM (~16s), expect at least 100KB
    assert file_size > 100_000, f"Audio file too small: {file_size} bytes"


def test_procedural_audio_different_artists(client: TestClient):
    """Test that different artists produce different audio files."""
    artists_to_test = [
        (["Depeche Mode"], "dark", 120),
        (["Gary Numan"], "dystopian", 125),
    ]

    for artists, mood, tempo in artists_to_test:
        response = client.post(
            "/api/music/generate",
            json={
                "artist_influences": artists,
                "mood": mood,
                "tempo_bpm": tempo,
            },
            headers={"X-User-Id": "test-user"},
        )

        assert response.status_code == 200, f"Failed for artists: {artists}"
        data = response.json()

        # Check audio URL
        audio_url = data["fake_audio_url"]
        assert audio_url.startswith("/static/audio/music/")
        assert ".wav" in audio_url

        # Verify file exists
        filename = audio_url.split("/")[-1]
        static_dir = Path(__file__).parent.parent / "static" / "audio" / "music"
        file_path = static_dir / filename
        assert file_path.exists(), f"Audio file not found for artists {artists}"
