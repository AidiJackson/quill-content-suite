# Quillography Content Suite - Replit Configuration

## Project Overview

**Quillography Content Suite** is a comprehensive FastAPI backend application that provides AI-powered content creation, editing, campaign management, and media processing services.

### Key Features
- Written Content Generation (blogs, newsletters, social posts, campaigns)
- Virality Engine for content scoring and optimization
- Video & Audio Processing (trimming, resizing, captions, pitch/tempo shifting)
- Project Management with versioning
- Interactive API documentation at `/docs`

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11
- **ORM**: SQLAlchemy 2.x
- **Database**: SQLite (development) / PostgreSQL (production)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Server**: Uvicorn
- **Testing**: pytest + HTTPX

## Replit Setup

### Environment Configuration

The application uses default configuration values that work out of the box:

- **Server Host**: 0.0.0.0 (required for Replit)
- **Server Port**: 5000 (Replit's exposed port)
- **Database**: SQLite (`quillography.db`) in development
- **CORS**: Configured to allow all origins for Replit proxy
- **AI Service**: Uses fake/deterministic AI client by default (no API key needed)

### Optional Environment Variables

If you need to customize settings, you can set these environment variables in Replit Secrets:

- `OPENAI_API_KEY` - Your OpenAI API key (if using real AI instead of fake client)
- `USE_FAKE_AI` - Set to `false` to use real OpenAI client (default: `true`)
- `DATABASE_URL` - Custom database URL (default: `sqlite:///./quillography.db`)
- `ENVIRONMENT` - Environment name (default: `development`)
- `DEBUG` - Enable debug mode (default: `true`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

### Running the Application

The FastAPI server runs automatically via the configured workflow:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

The API is accessible at:
- Development: Via the Replit webview
- Interactive Docs: `/docs` (Swagger UI)
- Alternative Docs: `/redoc` (ReDoc)
- Health Check: `/health`

### Project Structure

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
├── requirements.txt        # Python dependencies
├── Makefile               # Development commands
└── quillography.db        # SQLite database (gitignored)
```

## API Endpoints

### Content Generation
- `POST /content/blog` - Generate blog posts
- `POST /content/newsletter` - Generate newsletters
- `POST /content/post` - Generate social media posts
- `POST /content/campaign` - Generate campaigns

### Virality Engine
- `POST /virality/score` - Score content virality
- `POST /virality/optimize` - Optimize content for engagement
- `POST /virality/rewrite` - Rewrite content for better virality

### Media Processing
- `POST /video/trim` - Trim videos
- `POST /video/resize` - Resize videos
- `POST /audio/pitch` - Shift audio pitch
- `POST /audio/tempo` - Adjust audio tempo

### Project Management
- `GET /projects` - List projects
- `POST /projects` - Create project
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### System
- `GET /health` - Health check endpoint
- `GET /` - Welcome message with API info

## Development

### Database Migrations

The application creates database tables on startup via `init_db()` in `app/main.py`. The initial migration has already been applied.

To create and apply new migrations manually:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

**Note**: For production deployments, you should run `alembic upgrade head` before starting the server to ensure the database schema is up to date.

### Running Tests

```bash
pytest -v
```

### Code Quality

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
ruff check app/ tests/
```

## Deployment

The application is configured for **autoscale deployment** on Replit in the `.replit` file:

```toml
[deployment]
deploymentTarget = "autoscale"
run = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

When you publish this Repl:
- The server will automatically scale based on traffic
- The API will be accessible via your custom Replit domain
- Interactive documentation will be available at `/docs`

### Production Considerations

For production deployments:
1. **Database**: Consider using PostgreSQL instead of SQLite for production
   - Update `DATABASE_URL` environment variable
   - Run `alembic upgrade head` to apply migrations before first start
2. **API Keys**: Set proper environment variables for external services
   - Set `OPENAI_API_KEY` if using real AI client
   - Set `USE_FAKE_AI=false` to enable OpenAI integration
3. **Security**: 
   - Enable API key authentication if needed (`API_KEY_ENABLED=true`)
   - Configure specific CORS origins instead of wildcard `*`
   - Update `CORS_ORIGINS` to only include trusted domains
4. **Environment**: Set `ENVIRONMENT=production` and `DEBUG=false`

## Recent Changes

- **2025-11-13**: Initial Replit setup
  - Configured Python 3.11 environment
  - Updated CORS to allow Replit proxy domains
  - Changed default port to 5000 for Replit
  - Configured autoscale deployment
  - Created workflow for FastAPI server
  - Database migrations completed successfully

## Architecture

### Service Layer Pattern
- **Routes**: Handle HTTP requests and responses
- **Services**: Business logic isolated from routes
- **Models**: Database schema (SQLAlchemy ORM)
- **Schemas**: Request/response validation (Pydantic)
- **Dependencies**: Reusable components via FastAPI DI

### AI Client Architecture
The system uses a pluggable AI client pattern:
- **FakeAIClient**: Deterministic responses for testing (default)
- **OpenAIAIClient**: OpenAI integration (requires API key)

Switch between clients via `USE_FAKE_AI` environment variable.

## Support & Documentation

- API Documentation: `/docs` endpoint (Swagger UI)
- Project README: `README.md`
- API Reference: `API_REFERENCE.md`
- Roadmap: `CONTENT_SUITE_ROADMAP.md`
- UI Brief: `UI_BRIEF_FIGMA.md`

## Notes

- The fake AI client provides deterministic responses, perfect for testing and development
- All API endpoints return JSON responses
- The application uses SQLite by default for easy development
- Database file (`quillography.db`) is created automatically
- All database tables are created on first startup
