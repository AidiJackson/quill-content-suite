"""Tests for newsletter generation endpoints."""

import pytest


def test_generate_newsletter(client, headers):
    """Test newsletter generation."""
    payload = {
        "subject": "Weekly Tech Updates",
        "topics": ["AI", "Cloud Computing", "Cybersecurity"],
        "tone": "professional",
    }

    response = client.post("/content/newsletter", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["subject"] == "Weekly Tech Updates"
    assert "preview_text" in data
    assert "sections" in data
    assert "cta" in data
    assert "word_count" in data
    assert len(data["sections"]) > 0
