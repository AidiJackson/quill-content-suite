"""Tests for audio processing endpoints."""

import pytest


def test_cleanup_audio(client, headers):
    """Test audio cleanup."""
    payload = {"input_url": "https://example.com/audio.mp3"}

    response = client.post("/audio/cleanup", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "output_url" in data


def test_pitch_shift(client, headers):
    """Test pitch shifting."""
    payload = {"input_url": "https://example.com/audio.mp3", "semitones": 3}

    response = client.post("/audio/pitch", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "output_url" in data
    assert "semitones" in data
    assert data["semitones"] == 3


def test_tempo_shift(client, headers):
    """Test tempo shifting."""
    payload = {"input_url": "https://example.com/audio.mp3", "percent": 120}

    response = client.post("/audio/tempo", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "output_url" in data
    assert "tempo_percent" in data
    assert data["tempo_percent"] == 120


def test_extract_audio(client, headers):
    """Test audio extraction from video."""
    payload = {"input_url": "https://example.com/video.mp4"}

    response = client.post("/audio/extract", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "output_url" in data
    assert "duration" in data
