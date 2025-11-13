"""Tests for virality scoring endpoints."""

import pytest


def test_score_content(client, headers):
    """Test content virality scoring."""
    payload = {
        "text": "🔥 You won't believe this amazing productivity hack! Here's what changed my life forever...",
    }

    response = client.post("/virality/score", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "hook_score" in data
    assert "structure_score" in data
    assert "niche_score" in data
    assert "overall_score" in data
    assert "predicted_engagement" in data
    assert "recommendations" in data

    assert 0 <= data["hook_score"] <= 100
    assert 0 <= data["structure_score"] <= 100
    assert 0 <= data["niche_score"] <= 100
    assert 0 <= data["overall_score"] <= 100


def test_rewrite_for_virality(client, headers):
    """Test virality-focused rewriting."""
    payload = {
        "text": "I learned about productivity today.",
        "target_platform": "twitter",
    }

    response = client.post("/virality/rewrite", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "original_text" in data
    assert "rewritten_text" in data
    assert "original_score" in data
    assert "improved_score" in data
    assert "improvements" in data

    assert data["original_text"] == payload["text"]
