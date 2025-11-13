"""Tests for campaign generation endpoints."""

import pytest


def test_generate_campaign(client, headers):
    """Test campaign generation."""
    payload = {
        "goal": "Increase product awareness",
        "steps": 5,
        "audience": "Tech professionals",
    }

    response = client.post("/content/campaign", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["goal"] == "Increase product awareness"
    assert data["audience"] == "Tech professionals"
    assert "steps" in data
    assert len(data["steps"]) == 5
    assert "total_duration_days" in data

    for step in data["steps"]:
        assert "step_number" in step
        assert "subject" in step
        assert "content" in step
        assert "delay_days" in step


def test_expand_content(client, headers):
    """Test content expansion."""
    payload = {"text": "AI is transforming the world.", "target_length": "double"}

    response = client.post("/content/expand", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "original_length" in data
    assert "expanded_length" in data
    assert "content" in data
    assert data["expanded_length"] > data["original_length"]


def test_shorten_content(client, headers):
    """Test content shortening."""
    long_text = "This is a very long piece of text that needs to be shortened. " * 10

    payload = {"text": long_text, "target_length": 50}

    response = client.post("/content/shorten", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "original_length" in data
    assert "shortened_length" in data
    assert "content" in data


def test_rewrite_content(client, headers):
    """Test content rewriting."""
    payload = {
        "text": "Make this more engaging",
        "instructions": "Add excitement and energy",
    }

    response = client.post("/content/rewrite", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "original" in data
    assert "rewritten" in data
    assert data["original"] == payload["text"]
