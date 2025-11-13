"""Tests for blog generation endpoints."""

import pytest


def test_generate_blog(client, headers):
    """Test blog generation."""
    payload = {
        "topic": "AI and Machine Learning",
        "style_profile": {"tone": "professional", "length": "medium"},
    }

    response = client.post("/content/blog", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "title" in data
    assert "content" in data
    assert "word_count" in data
    assert (
        "AI and Machine Learning" in data["title"]
        or "AI and Machine Learning" in data["content"]
    )


def test_generate_blog_with_project(client, headers):
    """Test blog generation with project saving."""
    # Create project first
    project_payload = {
        "user_id": "test-user-123",
        "title": "Test Project",
        "description": "Test project for blog",
    }
    project_response = client.post("/projects", json=project_payload, headers=headers)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Generate blog with project
    blog_payload = {
        "topic": "Python Programming",
        "project_id": project_id,
    }

    response = client.post("/content/blog", json=blog_payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["saved_item_id"] is not None


def test_generate_outline(client, headers):
    """Test outline generation."""
    payload = {"topic": "Content Marketing Strategy", "sections": 7}

    response = client.post("/content/outline", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["topic"] == "Content Marketing Strategy"
    assert "sections" in data
    assert len(data["sections"]) == 7
