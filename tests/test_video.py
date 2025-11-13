"""Tests for video processing endpoints."""

import pytest


def test_trim_video(client, headers):
    """Test video trimming."""
    payload = {
        "input_url": "https://example.com/video.mp4",
        "start_time": 10.0,
        "end_time": 30.0,
    }

    response = client.post("/video/trim", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "output_url" in data
    assert "duration" in data
    assert data["duration"] == 20.0


def test_generate_captions(client, headers):
    """Test caption generation."""
    payload = {"input_url": "https://example.com/video.mp4"}

    response = client.post("/video/captions", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "srt_content" in data
    assert "caption_count" in data
    assert data["caption_count"] > 0


def test_resize_video(client, headers):
    """Test video resizing."""
    payload = {
        "input_url": "https://example.com/video.mp4",
        "aspect_ratio": "9:16",
    }

    response = client.post("/video/resize", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "output_url" in data
    assert "aspect_ratio" in data
    assert data["aspect_ratio"] == "9:16"


def test_generate_shorts(client, headers):
    """Test shorts generation."""
    payload = {"input_url": "https://example.com/video.mp4", "count": 3}

    response = client.post("/video/shorts", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "clips" in data
    assert len(data["clips"]) == 3

    for clip in data["clips"]:
        assert "url" in clip
        assert "start_time" in clip
        assert "duration" in clip
