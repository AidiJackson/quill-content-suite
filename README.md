# Quillography Content Suite

> AI-powered content creation, editing, campaign management, and media processing service

## Overview

Quillography Content Suite is a comprehensive FastAPI backend that provides a unified platform for:

- **Written Content Generation**: Blogs, articles, newsletters, social posts, campaigns
- **Virality Engine**: Content scoring, optimization, and rewriting for maximum engagement
- **Video & Audio Processing**: Trimming, resizing, captions, pitch/tempo shifting (MVP stubs)
- **Project Management**: Organize content and media in projects with versioning

## Features

### Content Generation
- Blog post generation with customizable style profiles
- Newsletter creation with multiple sections
- Social media posts for LinkedIn, Twitter, Facebook, Reddit, Instagram
- Multi-step campaign sequences
- Content outlines and hooks
- Expand, shorten, and rewrite capabilities

### Virality Engine
- Multi-dimensional virality scoring (hook, structure, niche)
- Platform-specific optimization
- Engagement prediction
- Automated content improvement recommendations

### Media Processing (MVP)
- Video trimming and resizing
- Auto-caption generation (stub)
- Short-form clip extraction
- Audio extraction from video
- Pitch and tempo shifting
- Audio cleanup (stub)

### Project Management
- Create and manage content projects
- Store content items with versioning
- Media file management
- Full CRUD operations

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Database**: PostgreSQL / SQLite
- **Testing**: pytest + HTTPX
- **AI**: Fake client (deterministic) + OpenAI stub

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd quill-content-suite

# Install dependencies
make install

# Copy environment file
cp .env.example .env

# Run migrations
make migrate
```

### Running the Server

```bash
# Development mode
make run

# Or directly with uvicorn
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
pytest --cov=app tests/
```

## Project Structure

```
quill-content-suite/
├── app/
│   ├── api/
│   │   ├── routes/         # API endpoints
│   │   └── deps.py         # Dependencies (auth, DB)
│   ├── core/               # Configuration and logging
│   ├── db/                 # Database setup
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── utils/              # Utilities
│   └── main.py             # FastAPI app
├── alembic/                # Database migrations
├── tests/                  # Test suite
├── requirements.txt
├── Makefile
└── README.md
```

## Configuration

Configure the application via `.env`:

```env
# Application
APP_NAME=Quillography Content Suite
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=sqlite:///./quillography.db

# AI Service
USE_FAKE_AI=true
OPENAI_API_KEY=your-key-here

# CORS
CORS_ORIGINS=http://localhost:3000
```

## API Reference

See [API_REFERENCE.md](./API_REFERENCE.md) for detailed endpoint documentation.

### Key Endpoints

- `POST /content/blog` - Generate blog posts
- `POST /content/newsletter` - Generate newsletters
- `POST /content/post` - Generate social media posts
- `POST /content/campaign` - Generate campaigns
- `POST /virality/score` - Score content virality
- `POST /video/trim` - Trim videos
- `POST /audio/pitch` - Shift audio pitch
- `GET /projects` - List projects
- `POST /projects` - Create project

## Development

### Code Quality

```bash
# Format code
make format

# Lint code
make lint
```

### Database Migrations

```bash
# Create a new migration
make makemigration

# Apply migrations
make migrate
```

### Testing Strategy

The test suite covers:
- All API endpoints
- Content generation with deterministic output
- Virality scoring
- Video/audio processing
- Project CRUD operations

## Deployment

### Production Checklist

1. Set `ENVIRONMENT=production` in `.env`
2. Use PostgreSQL instead of SQLite
3. Configure proper `OPENAI_API_KEY`
4. Enable API key authentication: `API_KEY_ENABLED=true`
5. Set strong `API_KEY`
6. Configure CORS origins appropriately
7. Run migrations: `make migrate`
8. Use a process manager (e.g., systemd, supervisor)

### Example Production Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Architecture

### Service Layer Pattern

- **Services**: Business logic isolated from routes
- **Repositories**: Data access through SQLAlchemy ORM
- **Schemas**: Request/response validation with Pydantic
- **Dependencies**: Reusable components via FastAPI DI

### AI Client Architecture

The system uses a pluggable AI client pattern:

- `FakeAIClient`: Deterministic responses for testing
- `OpenAIAIClient`: OpenAI integration (currently falls back to Fake)

Switch between clients via `USE_FAKE_AI` environment variable.

## Roadmap

See [CONTENT_SUITE_ROADMAP.md](./CONTENT_SUITE_ROADMAP.md) for future plans.

## Documentation

- [API Reference](./API_REFERENCE.md)
- [MVP Scope](./CONTENT_SUITE_SCOPE.md)
- [Roadmap](./CONTENT_SUITE_ROADMAP.md)
- [UI Brief](./UI_BRIEF_FIGMA.md)
- [Workflow Template](./WORKFLOW_TEMPLATE.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Format code: `make format`
6. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open a GitHub issue.
