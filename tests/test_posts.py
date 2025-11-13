"""Tests for social post generation endpoints."""

import pytest


def test_generate_social_posts(client, headers):
    """Test social post generation."""
    payload = {
        "topic": "Productivity Tips",
        "platforms": ["linkedin", "twitter"],
        "include_hooks": True,
    }

    response = client.post("/content/post", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "posts" in data
    assert len(data["posts"]) == 2

    for post in data["posts"]:
        assert "platform" in post
        assert "content" in post
        assert "character_count" in post
        assert "hashtags" in post


def test_generate_hooks(client, headers):
    """Test hook generation."""
    payload = {"topic": "Digital Marketing", "count": 5}

    response = client.post("/content/hooks", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "hooks" in data
    assert len(data["hooks"]) == 5
    assert all(isinstance(hook, str) for hook in data["hooks"])
