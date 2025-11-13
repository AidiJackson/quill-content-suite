# Quillography Content Suite - API Reference

Base URL: `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/docs`

---

## Authentication

All endpoints require the `X-User-Id` header:

```http
X-User-Id: your-user-id
```

Optional API key (if enabled):

```http
X-API-Key: your-api-key
```

---

## Health & Status

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Quillography Content Suite",
  "environment": "development"
}
```

### GET /

Root endpoint with API information.

**Response:**
```json
{
  "message": "Welcome to Quillography Content Suite",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## Projects

### POST /projects

Create a new content project.

**Request Body:**
```json
{
  "user_id": "user-123",
  "title": "My Content Project",
  "description": "Project for blog content"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "user_id": "user-123",
  "title": "My Content Project",
  "description": "Project for blog content",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### GET /projects

List all projects for the current user.

**Query Parameters:**
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=100): Maximum records to return

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "user_id": "user-123",
    "title": "My Content Project",
    "description": "Project for blog content",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET /projects/{project_id}

Get a specific project.

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "user_id": "user-123",
  "title": "My Content Project",
  "description": "Project for blog content",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PATCH /projects/{project_id}

Update a project.

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description"
}
```

**Response:** `200 OK`

### DELETE /projects/{project_id}

Delete a project.

**Response:** `204 No Content`

### GET /projects/{project_id}/content

List all content items for a project.

**Query Parameters:**
- `skip` (int, default=0)
- `limit` (int, default=100)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "project_id": "uuid",
    "type": "blog",
    "title": "Blog Title",
    "content": "Blog content...",
    "metadata": {},
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET /projects/{project_id}/media

List all media files for a project.

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "project_id": "uuid",
    "type": "video",
    "url": "https://example.com/video.mp4",
    "metadata": {},
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

## Content Generation

### POST /content/blog

Generate a blog post.

**Request Body:**
```json
{
  "topic": "AI and Machine Learning",
  "style_profile": {
    "tone": "professional",
    "voice": "authoritative",
    "length": "medium"
  },
  "keywords": ["AI", "ML", "automation"],
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "title": "The Ultimate Guide to AI and Machine Learning",
  "content": "# The Ultimate Guide...",
  "word_count": 1200,
  "metadata": {
    "style": {...},
    "generated_by": "FakeAI"
  },
  "saved_item_id": "uuid" // if project_id provided
}
```

### POST /content/outline

Generate a content outline.

**Request Body:**
```json
{
  "topic": "Content Marketing Strategy",
  "sections": 7,
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "topic": "Content Marketing Strategy",
  "sections": [
    "Introduction to Content Marketing Strategy",
    "Section 1: Key Aspect of Content Marketing Strategy",
    ...
  ],
  "saved_item_id": "uuid"
}
```

### POST /content/newsletter

Generate a newsletter.

**Request Body:**
```json
{
  "subject": "Weekly Tech Updates",
  "topics": ["AI", "Cloud Computing", "Cybersecurity"],
  "tone": "professional",
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "subject": "Weekly Tech Updates",
  "preview_text": "This week's insights on AI, Cloud Computing...",
  "sections": [
    {
      "heading": "Deep Dive: AI",
      "content": "Analysis of AI..."
    }
  ],
  "cta": "Read more on our blog",
  "word_count": 150,
  "saved_item_id": "uuid"
}
```

### POST /content/post

Generate social media posts.

**Request Body:**
```json
{
  "topic": "Productivity Tips",
  "platforms": ["linkedin", "twitter", "instagram"],
  "include_hooks": true,
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "posts": [
    {
      "platform": "linkedin",
      "content": "🔥 Hot take on Productivity Tips...",
      "character_count": 250,
      "hashtags": ["productivity", "tips", "work"]
    }
  ],
  "saved_item_ids": ["uuid1", "uuid2", "uuid3"]
}
```

### POST /content/hooks

Generate attention-grabbing hooks.

**Request Body:**
```json
{
  "topic": "Digital Marketing",
  "count": 5,
  "platform": "twitter" // optional
}
```

**Response:** `200 OK`
```json
{
  "hooks": [
    "🔥 You won't believe this about Digital Marketing",
    "The Digital Marketing secret nobody talks about",
    ...
  ]
}
```

### POST /content/campaign

Generate a content campaign.

**Request Body:**
```json
{
  "goal": "Increase product awareness",
  "steps": 5,
  "audience": "Tech professionals",
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "goal": "Increase product awareness",
  "audience": "Tech professionals",
  "steps": [
    {
      "step_number": 1,
      "subject": "Step 1: Moving towards Increase product awareness",
      "content": "This is step 1...",
      "delay_days": 0
    }
  ],
  "total_duration_days": 12,
  "saved_item_id": "uuid"
}
```

### POST /content/expand

Expand content.

**Request Body:**
```json
{
  "text": "AI is transforming the world.",
  "target_length": "double"
}
```

**Response:** `200 OK`
```json
{
  "original_length": 28,
  "expanded_length": 150,
  "content": "AI is transforming the world. Furthermore..."
}
```

### POST /content/shorten

Shorten content.

**Request Body:**
```json
{
  "text": "Long text here...",
  "target_length": 50 // optional
}
```

**Response:** `200 OK`
```json
{
  "original_length": 500,
  "shortened_length": 50,
  "content": "Shortened text..."
}
```

### POST /content/rewrite

Rewrite content with instructions.

**Request Body:**
```json
{
  "text": "Original content",
  "instructions": "Make it more engaging and exciting"
}
```

**Response:** `200 OK`
```json
{
  "original": "Original content",
  "rewritten": "[Rewritten with: Make it more engaging and exciting]\n\nOriginal content"
}
```

---

## Virality

### POST /virality/score

Score content for virality potential.

**Request Body:**
```json
{
  "text": "🔥 You won't believe this amazing productivity hack!",
  "content_item_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "hook_score": 85,
  "structure_score": 78,
  "niche_score": 82,
  "overall_score": 81,
  "predicted_engagement": 850.0,
  "recommendations": [
    "Add more emotional triggers",
    "Include a clear call-to-action",
    "Use more specific examples"
  ],
  "saved_score_id": "uuid"
}
```

### POST /virality/rewrite

Rewrite content to maximize virality.

**Request Body:**
```json
{
  "text": "I learned about productivity today.",
  "target_platform": "twitter" // optional
}
```

**Response:** `200 OK`
```json
{
  "original_text": "I learned about productivity today.",
  "rewritten_text": "[Rewritten with: Rewrite to maximize engagement...]\n\nI learned about productivity today.",
  "original_score": 45,
  "improved_score": 78,
  "improvements": [
    "Improved hook strength",
    "Better content structure"
  ]
}
```

---

## Video Processing

### POST /video/trim

Trim a video.

**Request Body:**
```json
{
  "input_url": "https://example.com/video.mp4",
  "start_time": 10.0,
  "end_time": 30.0,
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "output_url": "https://fake-storage.example.com/trimmed_10.0_30.0.mp4",
  "duration": 20.0,
  "saved_media_id": "uuid"
}
```

### POST /video/captions

Generate captions for a video.

**Request Body:**
```json
{
  "input_url": "https://example.com/video.mp4"
}
```

**Response:** `200 OK`
```json
{
  "srt_content": "1\n00:00:00,000 --> 00:00:05,000\nCaption text...",
  "caption_count": 3
}
```

### POST /video/resize

Resize video to target aspect ratio.

**Request Body:**
```json
{
  "input_url": "https://example.com/video.mp4",
  "aspect_ratio": "9:16",
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "output_url": "https://fake-storage.example.com/resized_9_16.mp4",
  "aspect_ratio": "9:16",
  "saved_media_id": "uuid"
}
```

### POST /video/shorts

Generate short clips from a video.

**Request Body:**
```json
{
  "input_url": "https://example.com/video.mp4",
  "count": 3,
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "clips": [
    {
      "url": "https://fake-storage.example.com/short_1.mp4",
      "start_time": 0,
      "duration": 30,
      "score": 85
    }
  ],
  "saved_media_ids": ["uuid1", "uuid2", "uuid3"]
}
```

---

## Audio Processing

### POST /audio/cleanup

Clean up audio (noise reduction).

**Request Body:**
```json
{
  "input_url": "https://example.com/audio.mp3",
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "output_url": "https://fake-storage.example.com/cleaned_audio.mp3",
  "saved_media_id": "uuid"
}
```

### POST /audio/pitch

Shift audio pitch.

**Request Body:**
```json
{
  "input_url": "https://example.com/audio.mp3",
  "semitones": 3,
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "output_url": "https://fake-storage.example.com/pitched_3.mp3",
  "semitones": 3,
  "saved_media_id": "uuid"
}
```

### POST /audio/tempo

Shift audio tempo.

**Request Body:**
```json
{
  "input_url": "https://example.com/audio.mp3",
  "percent": 120,
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "output_url": "https://fake-storage.example.com/tempo_120.mp3",
  "tempo_percent": 120,
  "saved_media_id": "uuid"
}
```

### POST /audio/extract

Extract audio from video.

**Request Body:**
```json
{
  "input_url": "https://example.com/video.mp4",
  "project_id": "uuid" // optional
}
```

**Response:** `200 OK`
```json
{
  "output_url": "https://fake-storage.example.com/extracted_audio.mp3",
  "duration": 180.0,
  "saved_media_id": "uuid"
}
```

---

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "User ID header is required"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting in MVP. Recommended for production:

- 100 requests per minute per user
- 1000 requests per hour per user

---

## Pagination

Endpoints returning lists support pagination:

**Query Parameters:**
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=100, max=1000): Maximum records to return

**Example:**
```
GET /projects?skip=20&limit=10
```

---

## Webhooks (Future)

Not implemented in MVP. Planned for Phase 3.

---

## SDKs (Future)

Official SDKs planned for:
- Python
- JavaScript/TypeScript
- Go

---

## Changelog

### v1.0.0 (MVP)
- Initial release
- All core endpoints
- Fake AI client
- Video/audio stubs
- Project management

---

For interactive API exploration, visit `/docs` when running the server.
