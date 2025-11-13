"""Tests for project management endpoints."""

import pytest


def test_create_project(client, headers):
    """Test project creation."""
    payload = {
        "user_id": "test-user-123",
        "title": "My Content Project",
        "description": "A test project for content creation",
    }

    response = client.post("/projects", json=payload, headers=headers)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "My Content Project"
    assert data["description"] == "A test project for content creation"
    assert data["user_id"] == "test-user-123"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_projects(client, headers):
    """Test listing projects."""
    # Create some projects first
    for i in range(3):
        payload = {
            "user_id": "test-user-123",
            "title": f"Project {i + 1}",
            "description": f"Test project {i + 1}",
        }
        client.post("/projects", json=payload, headers=headers)

    # List projects
    response = client.get("/projects", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_get_project(client, headers):
    """Test getting a specific project."""
    # Create project
    create_payload = {
        "user_id": "test-user-123",
        "title": "Specific Project",
        "description": "Test",
    }
    create_response = client.post("/projects", json=create_payload, headers=headers)
    project_id = create_response.json()["id"]

    # Get project
    response = client.get(f"/projects/{project_id}", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == project_id
    assert data["title"] == "Specific Project"


def test_update_project(client, headers):
    """Test updating a project."""
    # Create project
    create_payload = {
        "user_id": "test-user-123",
        "title": "Original Title",
        "description": "Original description",
    }
    create_response = client.post("/projects", json=create_payload, headers=headers)
    project_id = create_response.json()["id"]

    # Update project
    update_payload = {
        "title": "Updated Title",
        "description": "Updated description",
    }
    response = client.patch(
        f"/projects/{project_id}", json=update_payload, headers=headers
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"


def test_delete_project(client, headers):
    """Test deleting a project."""
    # Create project
    create_payload = {
        "user_id": "test-user-123",
        "title": "To Delete",
        "description": "Test",
    }
    create_response = client.post("/projects", json=create_payload, headers=headers)
    project_id = create_response.json()["id"]

    # Delete project
    response = client.delete(f"/projects/{project_id}", headers=headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/projects/{project_id}", headers=headers)
    assert get_response.status_code == 404


def test_list_project_content(client, headers):
    """Test listing project content items."""
    # Create project
    project_payload = {
        "user_id": "test-user-123",
        "title": "Content Project",
        "description": "Test",
    }
    project_response = client.post("/projects", json=project_payload, headers=headers)
    project_id = project_response.json()["id"]

    # Create some content
    blog_payload = {"topic": "Test Topic", "project_id": project_id}
    client.post("/content/blog", json=blog_payload, headers=headers)

    # List content
    response = client.get(f"/projects/{project_id}/content", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_list_project_media(client, headers):
    """Test listing project media files."""
    # Create project
    project_payload = {
        "user_id": "test-user-123",
        "title": "Media Project",
        "description": "Test",
    }
    project_response = client.post("/projects", json=project_payload, headers=headers)
    project_id = project_response.json()["id"]

    # Create some media
    video_payload = {
        "input_url": "https://example.com/video.mp4",
        "start_time": 0.0,
        "end_time": 10.0,
        "project_id": project_id,
    }
    client.post("/video/trim", json=video_payload, headers=headers)

    # List media
    response = client.get(f"/projects/{project_id}/media", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
